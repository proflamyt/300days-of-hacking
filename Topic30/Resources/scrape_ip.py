#!/usr/bin/env python3

import dns.resolver
import collections
import threading
import traceback
import argparse
import ipwhois
import random
import sys
import os
import re

import utils

# defaults
default_nameserver = '8.8.8.8'
default_max_threads = 6

def get_range_info(ip):
    """
    Get whois IP range and ASN/network information for an IP address

    :param ip: IP to get info for
    :return: Dictionary containing range info in the format {asn_cidr,
             asn_description, network_cidr, network_name,
             contacts: [{name, email: [], phone: [], address: []}...]
    """

    whois = ipwhois.IPWhois(ip)
    # asn_methods is supposed to default to ['dns', 'whois', 'http'] but the
    # code sets a local variable called 'lookups' and later checks if the
    # asn_methods parameter is None and throws a 'Permutations not allowed'
    # exception.
    #
    # as a result, if the dns lookup method fails it never gets to the other
    # two methods. asn_methods basically defaults to ['dns'].
    result = whois.lookup_rdap(asn_methods=['dns', 'whois', 'http'])

    #import pprint
    #pprint.pprint(result)

    asn_info = {'asn_cidr': result['asn_cidr'],
                'asn_description': result['asn_description'],
                'asn_country': result['asn_country_code'],
                'network_cidr': result['network']['cidr'],
                'network_name': result['network']['name'],
                'contacts': []}

    # add contacts
    if 'objects' in result:
        for object_name, object_info in result['objects'].items():
            if 'contact' in object_info:
                object_contact = object_info['contact']
                contact = {'name': object_contact['name'], 'email': None,
                           'phone': None, 'address': None}

                # these ones need to be flattened out a bit
                for key in ('email', 'phone', 'address'):
                    if key in object_contact and object_contact[key]:
                        values = [item['value'] for item in object_contact[key]]
                        contact[key] = list(set(values))
                asn_info['contacts'].append(contact)

    return asn_info

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_argument_group('input arguments')
    group.add_argument('item', nargs='*', help='IP address, CIDR range, or domain name to perform recon on')
    group.add_argument('-f', '--file', action='append', help='file containing IP addresses, CIDR ranges, and/or domain names to perform recon on')

    group = parser.add_argument_group('dns arguments')
    group.add_argument('-n', '--nameserver', default=[default_nameserver], action='append',
            help='use these nameservers (default: {})'.format(default_nameserver))
    group.add_argument('--system-nameservers', action='store_true',
            help='use system nameservers')
    group.add_argument('-u', '--udp', action='store_true',
            help='use udp instead of tcp to resolve domains')

    group = parser.add_argument_group('threading arguments')
    group.add_argument('-t', '--max-threads', type=int, default=default_max_threads,
            help='maximum number of threads to use at once (default: {})'.format(default_max_threads))

    group = parser.add_argument_group('output arguments')
    group.add_argument('-o', '--output', help='tee output to a file')
    group.add_argument('-q', '--quiet', action='store_true', help='do not print status messages to stderr')
    group.add_argument('-D', '--debug', action='store_true', help='enable debug output')
    args = parser.parse_args()

    # -D/--debug
    if args.debug:
        # enable debug messages
        utils.enable_debug()

    # -q/--quiet
    if args.quiet:
        # disable prefixed stderr messages
        utils.disable_status()

    # -o/--output
    if args.output:
        # set log file
        utils.set_log(args.output)

    # --system-nameservers
    if not args.system_nameservers:
        # -n/--nameserver
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = args.nameserver
        dns.resolver.default_resolver.rotate = True

    items = set()

    # <item>
    if args.item:
        items |= set(args.item)

    # -f/--file
    items |= set(utils.file_items(args.file))

    if not items:
        utils.die('Provide some domain names, IP addresses, or CIDR ranges')

    # {ip: set(parent_domain...)}
    parent_domains = collections.defaultdict(set)

    def resolve_items(items):
        for ip, item, ports in utils.resolve_to_ips(items, tcp=not args.udp):
            # track parent items
            if ip != item and not utils.is_cidr(item):
                parent_domains[ip].add(item)

            # handle errors
            if isinstance(ip, Exception):
                exception = ip
                utils.bad('Failed to resolve {}: {}'.format(item, str(exception)))
                utils.debug_exception(exception)
                continue

            yield ip

    # shuffle the items. may make slightly more efficient use of the result cache
    random.shuffle(list(items))

    ips = resolve_items(items)

    # check to make sure domains resolved
    ips = utils.check_iterator(ips)
    if not ips:
        utils.die('No domains resolved. No IP addresses to perform recon on.')

    # since we need to deduplicate ASNs and work with cached results the result
    # data is modified directly in each thread.
    # {asn_cidr: {info: {...}, ips: set(ip...)}
    ranges = collections.defaultdict(dict)
    # lock for ranges
    ranges_lock = threading.Lock()

    # produce ' (domain)' note for an IP if it has a parent domain
    def domain_note(ip):
        return ' ({})'.format(' '.join(parent_domains[ip])) if ip in parent_domains else ''

    def thread_helper(ip):
        with ranges_lock:
            existing_cidr = utils.find_cidr(ranges.keys(), ip)
            if existing_cidr:
                utils.info('Using known ASN {} for {}{}'.format(existing_cidr, ip, domain_note(ip)))
                ranges[existing_cidr]['ips'].add(ip)
                return

        utils.info('Getting ASN info for {}{}'.format(ip, domain_note(ip)))

        try:
            result = get_range_info(ip)
        except Exception as e:
            utils.bad('Failed to get ASN info for {}: {}'.format(ip, str(e)))
            utils.debug(traceback.format_exc(limit=6))
            return

        with ranges_lock:
            asn_cidr = result['asn_cidr']
            if asn_cidr in ranges:
                # another thread has already seen this ASN
                ranges[asn_cidr]['ips'].add(ip)
            else:
                # this is the first thread to see this ASN
                ranges[asn_cidr]['info'] = result
                ranges[asn_cidr]['ips'] = {ip}

    for ip, result in utils.threadify(thread_helper, ips, max_threads=args.max_threads):
        if isinstance(result, Exception):
            # thread_helper should throw no Exceptions
            raise result

    if ranges:
        # print total
        utils.good('Found {} ASNs'.format(len(ranges)))
    else:
        # nothing found
        utils.bad('Found 0 ASNs. All ASN queries failed.')

    # display info grouped by ASN CIDR
    first_line = True
    for asn_cidr, metadata in ranges.items():
        # fencepost
        if not first_line:
            utils.log()
        else:
            first_line = False

        # asn and network info
        network_name = metadata['info']['network_name']
        network_cidr = metadata['info']['network_cidr']
        asn_desc = metadata['info']['asn_description']
        asn_country = metadata['info']['asn_country']

        utils.log('ASN CIDR: {}'.format(asn_cidr))
        utils.log('ASN description: {}'.format(asn_desc))
        utils.log('Network name: {}'.format(network_name))
        if network_cidr == asn_cidr:
            note = ' (same as ASN)'
        else:
            note = ''
        utils.log('Network CIDR(s): {}{}'.format(network_cidr.replace(',', ''), note))

        # contacts
        for contact in metadata['info']['contacts']:
            if contact['name'] or contact['email'] or contact['phone']:
                out = 'Contact:'
                if contact['name']:
                    out += ' {}'.format(contact['name'])
                if contact['email']:
                    out += ' {}'.format(' '.join(contact['email']))
                if contact['phone']:
                    out += ' {}'.format(' '.join(contact['phone']))
                utils.log(out)

        # hosts
        utils.log('Hosts ({}):'.format(len(metadata['ips'])))
        for ip in metadata['ips']:
            out = ' - {}'.format(ip)
            if ip in parent_domains:
                # add domain info
                out += ' ({})'.format(' '.join(parent_domains[ip]))
            utils.log(out)

if __name__ == '__main__':
    main()