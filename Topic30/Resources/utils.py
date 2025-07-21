import traceback
import itertools
import socket
import enum
import sys

# third-party modules are imported in their calling functions. this allows
# utils.py to be used for multiple scripts without cluttering up their
# dependencies lists.

def basedir(append=''):
    """
    Get the base directory of the caller. Optionally append a path to it.

    :param append: Path to append
    :return: Base directory with /<append> appended.
    """

    return os.path.realpath(os.path.dirname(__file__)) + '/' + append

def file_items(files):
    """
    Read a list of items from files

    :param files: File names to read (any iterable)
    :return: Generator producing items. Each item is strip()ed. Returns an
             empty generator if None or [] is passed.
    """

    if not files:
        return

    for fname in files:
        with open(fname, 'r') as fp:
            yield from (item.strip() for item in fp)

def resolve_domain(domain, tcp=True):
    """ 
    Resolve a domain to its IP addresses

    :param domain: Domain to resolve
    :param tcp: Use TCP to talk to the nameserver
    :return: Set of IP addresses for the domain. None if it's NoAnswer or
             NXDOMAIN. Throws all other resolution exceptions.
    """

    import dns.resolver

    try:
        ips = set([str(record) for record in dns.resolver.query(domain, 'A', tcp=tcp)])
        return ips
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return None

def is_ip(item):
    """
    Check if a string looks like an IP address

    :param item: String to check
    :return: True if item is an IP address
    """

    try:
        socket.inet_aton(item)
        return True
    except socket.error:
        return False

def is_cidr(item):
    """
    Check if a string looks like an CIDR range

    :param item: String to check
    :return: True if item is a CIDR range
    """

    import netaddr

    try:
        netaddr.IPNetwork(item)
        return True
    except netaddr.core.AddrFormatError:
        return False

def cidr_ips(cidr):
    """
    Get list of IP addresses for a CIDR

    :param cidr: CIDR to get IP addresses for
    :return: Generator producing IP addresses from the CIDR
    """

    import netaddr

    yield from (str(ip) for ip in netaddr.IPNetwork(cidr))

def find_cidr(cidrs, ip):
    """
    Find the CIDR for an IP address in a list of CIDRs. Returns the first CIDR
    if there are multiple.

    :param cidrs: List of CIDRs
    :param ip: IP address
    :return: CIDR or None
    """

    import netaddr

    for cidr in cidrs:
        if netaddr.IPAddress(ip) in netaddr.IPNetwork(cidr):
            return cidr

    return None

def resolve_to_ips(items, resolve_cidr=True, resolve_domains=True,
                   parse_ports=False, tcp=False):
    """
    Resolve an iterable of domain names, CIDR ranges, and IP addresses to IP
    addresses.

    :param items: Iterable of items
    :param resolve_cidr: Resolve CIDR ranges
    :param resolve_domains: Resolve domains
    :param parse_ports: Parse port ranges
    :param tcp: Use TCP for name resolution
    :return: Generator producing tuples containing: (ip, original_item,
             {ports}). If the IP returned is None resolution was not possible. If the IP
             returned is an Exception there was an error parsing or resolving the item.
    """

    for item in items:
        try:
            # parse out port ranges
            if parse_ports and ':' in item:
                item, *portranges = item.split(':')[0:]
                ports = set(parse_ranges(portranges))
            else:
                ports = None

            if is_ip(item):
                # it's an IP address
                yield (item, item, ports)
            elif is_cidr(item):
                # it's a CIDR range
                if resolve_cidr:
                    yield from ((ip, item, ports) for ip in cidr_ips(item))
                else:
                    exception = RuntimeError('CIDR range resolution is disabled. Could not resolve {}'.format(item))
                    yield (exception, item, ports)
            elif resolve_domains:
                # probably a domain name. resolve it
                debug('Resolving domain {}'.format(item))
                resolved_ips = resolve_domain(item, tcp=tcp)
                if resolved_ips:
                    yield from ((ip, item, ports) for ip in resolved_ips)
                else:
                    exception = RuntimeError('Failed to resolve domain')
                    yield (exception, item, ports)
            else:
                # resolve_domains is off and it wasn't an IP or CIDR
                exception = RuntimeError('Domain resolution is disabled. Could not resolve {}'.format(item))
                yield (exception, item, ports)
        except Exception as exception:
            yield (exception, item, None)

def port_pairs(pairs):
    """
    Produce (host, port) pairs for (host, ports) tuples.

    :param pairs: Iterable of tuples containing (host, ports) where ports is an iterable of ports.
    :return: Generator producing all possible (host, port) pairs
    """

    for pair in pairs:
        host, ports = pair
        for port in ports:
            yield host, port

def soup_up(response):
    """
    Get BeautifulSoup object for requests.get() response. Handles encoding
    correctly.

    :param response: Response to parse
    """

    if 'charset' in response.headers.get('content-type', '').lower():
        http_encoding = response.encoding
    else:
        http_encoding = None

    import bs4
    html_encoding = bs4.dammit.EncodingDetector.find_declared_encoding(response.content, is_html=True)
    encoding = html_encoding or http_encoding
    soup = bs4.BeautifulSoup(response.content, features='lxml', from_encoding=encoding)

    return soup

def rdns(ip, tcp=False):
    """
    Get PTR record for an IP address

    :param ip: IP to get PTR record for
    :param tcp: Use TCP to talk to the nameserver
    :return: PTR record or none
    """

    import dns.reversename
    import dns.resolver

    rev = dns.reversename.from_address(ip)
    try:
        record = str(dns.resolver.query(rev, 'PTR', tcp=tcp)[0]).rstrip('.')
        return record
    except dns.resolver.NXDOMAIN:
        return None

def threadify(function, items, max_threads=10, throw_exceptions=False,
        arg_items=False):
    """
    Threadpool helper. Automagically multi-threadifies a function with some items.
    Handles generators correctly by only submitting max_threads * 2 items to
    the threadpool at a time. Returns an iterator that produces (item, result)
    tuples in real-time.

    By default exceptions are returned in the results instead of thrown. See
    throw_exceptions.

    :param function: Function to execute on each item. Called like
                     function(item) by default. See arg_items for an
                     alternative.
    :param items: Iterable (or generator) of items to submit to the threadpool
    :param max_threads: Maximum number of threads to run at a time
    :param throw_exceptions: Throw exceptions instead of returning them.
                             Exception.item is set to the original item.
    :param arg_items: Each item is an iterable of positional arguments or a
                      dict of keyword arguments for the function. Function
                      calls become function(*item) or function(**item) if the
                      item is a dict.
    :return: Generator producing iter((item, result)...)
    """

    import concurrent.futures

    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_threads)
    futures = set()

    # There are certain generators, like range() that are iterable but not
    # iterators and produce repeating, never-depleting lists of numbers for
    # some reason. This fixes that problem.
    items = iter(items)

    # since there's no way to get the original item from a future we have to
    # use this helper.
    #
    # this also handles exceptions. we can't use future.exception() since we'd
    # have no way to associate items with their exceptions. this makes handling
    # results from threadify a bit more annoying but meh... I can't really
    # think of a better option.
    def thread_helper(item):
        try:
            if arg_items:
                if isinstance(item, dict):
                    result = function(**item)
                elif is_iterable(item):
                    result = function(*item)
                else:
                    raise RuntimeError('arg_items is set but item is not an iterable or dict')
            else:
                result = function(item)

            return item, result
        except Exception as exception:
            return item, exception

    running = True
    while running or futures:
        # submit to threadpool
        # only submits max_threads * 2 at a time, in case items is a big generator
        for item in items:
            future = thread_pool.submit(thread_helper, item)
            futures.add(future)

            if len(futures) > max_threads * 2:
                break
        else:
            running = False

        # now we wait for some futures to complete
        # in order to provide results to the caller in realtime we use FIRST_COMPLETED
        done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
        for future in done:
            exception = future.exception()
            if exception:
                # we should hopefully never reach this
                raise exception
            
            item, result = future.result()
            if throw_exceptions and isinstance(result, Exception):
                result.item = item
                raise result
            else:
                yield item, result

def is_iterable(item):
    """
    Determine if an item is iterable.

    :param item: Item to check
    :return: True if 'item' is iterable
    """

    try:
        # sometimes python tries to optimize out native types that aren't used
        null = iter(item)
        return True
    except TypeError:
        return False

def check_iterator(iterator):
    """
    Determine if an iterator is empty. For some reason Python doesn't allow you
    to peak at the first element of an iterator so this is pretty hacky.

    :param iterator: Iterator to check
    :return: An iterator containing the original values or None if empty
    """

    try:
        first = next(iterator)
        return itertools.chain([first], iterator)
    except StopIteration:
        return None

def is_int(value, base=10):
    """
    Determine if a string value is an integer.

    :param value: String to check
    :param base: Numeric base to check with (default: 10)
    :return: True if 'value' is an integer
    """

    try:
        # sometimes python tries to optimize out native types that aren't used
        null = int(value, base=base)
        return True
    except ValueError:
        return False

def parse_ranges(ranges, allow_unbounded=False):
    """
    Parse a list of number ranges.

    A number range looks like this: 1,5-7,30-32.
    This turns into iter([1, 5, 6, 7, 30, 31, 32]).

    A generator is returned. A range with no end will produce an infinite
    amount of numbers. For example: '5-' produces all numbers from 5 to
    infinity.

    :param ranges: Iterable of ranges to parse
    :return: Generator producing values from the parsed range
    """

    for r in ranges:
        for r2 in r.split(','):
            if '-' in r2:
                start, finish = r2.split('-')
                start = int(start)
                if finish:
                    # bounded range (start-finish)
                    finish = int(finish)
                    yield from range(start, finish + 1)
                elif allow_unbounded:
                    # infinite/unbounded range (start-)
                    value = start
                    while True:
                        yield value
                        value += 1
                else:
                    raise RuntimeError('unbounded range: {}'.format(r2))
            else:
                yield int(r2)

def combine_comma_lists(lists, sep=','):
    """
    Combine comma lists (multiple lists with items separated by commas).

    :param lists: List of comma-lists
    :param sep: Separator to use instead of comma
    :return: A single list of items
    """

    items = []
    for l in lists:
        items += l.split(sep)
    return items

def comma_list(items, sep=', '):
    """
    Make a nice comma list

    :param items: Items to combine
    :param sep: Separator to use instead of comma
    :return: Items separated by ', '
    """

    return ', '.join(items)

# print helpers
_disabled_groups = {'debug'}
_log_file = None
_status_stream = sys.stderr

def disable_groups(*groups):
    """
    Disable message groups

    :param groups: Groups to disable
    """

    global _disabled_groups

    _disabled_groups |= set(groups)

def enable_groups(*groups):
    """
    Enable message groups

    :param groups: Groups to enable
    """

    global _disabled_groups

    _disabled_groups -= set(groups)

def enable_debug():
    """
    Enable debug messages from utils.debug()
    """

    enable_groups('debug')

def disable_debug():
    """
    Disable debug messages from utils.debug()
    """

    disable_groups('debug')

def disable_status():
    """
    Disable status messages from utils.info(), utils.good(), utils.bad(),
    utils.subline(), utils.debug(), and utils.die()
    """

    disable_groups('info', 'good', 'bad', 'subline', 'debug')

def enable_status():
    """
    Enable status messages from utils.info(), utils.good(), utils.bad(),
    utils.subline(), utils.debug(), and utils.die()
    """

    enable_groups('info', 'good', 'bad', 'subline', 'debug')

def enable_terminal(stream=sys.stderr):
    """
    Enable logging messages to terminal

    :param stream: Stream to write to (default: sys.stderr)
    """

    global _status_stream

    _status_stream = stream

def disable_terminal():
    """
    Disable logging messages to terminal
    """

    global _status_stream

    _status_stream = None

def set_log(fname):
    """
    Write log messages to a file
    """

    global _log_file

    _log_file = fname

def disable_log():
    """
    Disable log file
    """

    global _log_file

    _log_file = None

def log(message='', group='other', color=None, status=False):
    """
    Log message to stderr and/or file, depending on settings

    :param message: Message to log
    :param group: Message group
    :param color: Message color. Passed directly to termcolor, if termcolor is installed
    :param status: Message is a status message. Print to stderr.
    """

    global _log_file
    global _status_stream
    global _disabled_groups

    if group in _disabled_groups:
        # messagr group is disabled
        return False

    if _status_stream:
        # print to terminal
        if color and _status_stream.isatty() and sys.platform.startswith('linux'):
            try:
                import termcolor
                terminal_message = termcolor.colored(message, color)
            except Exception as e:
                debug_exception(e)
                terminal_message = message
        else:
            terminal_message = message

        if status:
            print(terminal_message, file=_status_stream)
        else:
            print(terminal_message)

    if _log_file:
        # write to log file
        with open(_log_file, 'a+') as fp:
            fp.write(message + '\n')

    return True

def debug(message):
    """
    Log a debug message. Debug messages are disabled by default. Enable them
    with utils.enable_debug(). Disable them again with utils.disable_debug().

    :param message: Message to log
    """

    return log('[D] ' + message, group='debug', status=True)

def raw_debug(message):
    """
    Log a raw debug message. No prefix. See utils.debug().

    :param message: Message to log
    """

    return log(message, group='debug', status=True)

def info(message):
    """
    Log an info message.

    :param message: Message to log
    """

    return log('[.] ' + message, group='info', status=True)

def good(message, color=False):
    """
    Log a good message.

    :param message: Message to log
    """

    return log('[+] ' + message, group='good', color='green' if color else None, status=True)

def bad(message, color=False):
    """
    Log a bad message.

    :param message: Message to log
    """

    return log('[!] ' + message, group='bad', color='yellow' if color else None)

def die(message=None, code=1):
    """
    Log a bad message and exit.

    :param message: Message to log
    :param code: Process return code
    """

    if message:
        bad(message)
    sys.exit(code)

def subline(message):
    """
    Log an indented message.

    :param message: Message to log
    """

    return log('    ' + message, group='subline', status=True)

def exception_info(exception, limit=6):
    """
    Get multi-line info and stacktrace for an exception

    :param exception: Exception
    :param limit: Stackframe limit
    :return: Exception info from traceback
    """

    try:
        if isinstance(exception, Exception):
            raise exception
        else:
            # not an exception
            return None
    except:
        return traceback.format_exc(limit=limit)

    # weird exception. failed to raise
    return None

def debug_exception(exception, limit=6):
    """
    Print info for an exception if debug is enabled.

    :param exception: Exception
    :param limit: Stackframe limit
    """

    info = exception_info(exception, limit=limit)
    if info:
        raw_debug(info)