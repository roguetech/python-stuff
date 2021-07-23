from scapy.all import *

def get_flags(self):
        # Get SYN Only
        if pcap[TCP].flags.S and not (pcap[TCP].flags.A or pcap[TCP].flags.P):
            return 'S'

        # Get SYN-ACK
        if pcap[TCP].flags.S and pcap[TCP].flags.A and not (pcap[TCP].flags.P):
            return 'SA'

        # Get ACK Only
        if pcap[TCP].flags.A and not (pcap[TCP].flags.S or pcap[TCP].flags.P):
            return 'A'

        # Get RST
        if pcap[TCP].flags.R and not (pcap[TCP].flags.S or pcap[TCP].flags.A):
            return 'R'

def flags(pcap):
    #print("Flag is %s", pcap[TCP].flags)
    if pcap[TCP].flags.R and not (pcap[TCP].flags.S or pcap[TCP].flags.A or pcap[TCP].flags.P):
        print(pcap[TCP].flags)
        print('Only SYN Received %s', pcap[TCP].flags)
    '''
    if pcap[TCP].flags.A:
        print('ACK Received %s', pcap[TCP].flags)
    if pcap[TCP].flags.S and pcap[TCP].flags.A:
        print('SYNACK Received %s', pcap[TCP].flags)
    if pcap[TCP].flags.F:
        print('FIN Received %s', pcap[TCP].flags)
    '''
if __name__ == '__main__':
    sniff(filter="tcp", iface = "enp0s31f6",prn=flags)

    flag = get_flags()
    
    #sniff(iface = "enp0s31f6",prn=lambda x:x.show())




