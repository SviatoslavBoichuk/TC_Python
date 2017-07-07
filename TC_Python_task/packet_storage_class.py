import scapy.all as scapy
import threading
import time

PROTO_TCP = 'tcp'
ENCODE = 'utf-8'
PORT_NO = 80


class PacketStorage:
    """Class contain information about addressant
    and his packets, that need to send"""
    __addressant_name = ""
    __addressant_ip = ""

    def __init__(self, name, ip):
        """Initialize private class members"""
        self.__addressant_name = name
        self.__addressant_ip = ip
        self.__addressant_packets = []

    def add_packet(self, packet):
        """Save new addressant @packet to list"""
        self.__addressant_packets.append(packet)

    def get_addressant_packets(self):
        """Return all addressant packets"""
        return self.__addressant_packets

    def get_addressant_name(self):
        """Return addressant name"""
        return self.__addressant_name

    def __ping(self, repeat=1):
        """Send ICPM echo-request, to check if destination host available"""
        answer, no_answer = scapy.sr(scapy.IP(
            dst=self.__addressant_ip) / scapy.ICMP(),
                                     timeout=repeat)
        return bool(answer)

    def __sniff_packets(self, pack, repeat=1):
        """sniff packets to find out if @pckt was sent"""

        msg = pack.getlayer(scapy.Raw).load.decode(ENCODE)
        catched_packtes = scapy.sniff(filter=PROTO_TCP, timeout=repeat)

        # get catched packets and search packet that we sent
        for packet in catched_packtes:
            packet_load = packet.getlayer(scapy.Raw).load

            # check destination ip and payload
            if packet.getlayer(scapy.IP).dst == self.__addressant_ip and \
                            packet_load.decode(ENCODE) == msg:
                print('Sent packet \'{}\' to {}'.format(msg, self.__addressant_name))
            else:
                print('Something went wrong...')

    def send_packets(self):
        """Send all packets"""

        for line in self.__addressant_packets:
            # ping before send message
            if self.__ping():
                # if ping ok - send packets and try to catch sent packets
                packet = scapy.IP(dst=self.__addressant_ip) / scapy.TCP(sport=PORT_NO, dport=PORT_NO)
                packet.payload = '\n'.join(self.__addressant_packets)
                # start sniffing sended packet in another thread
                thread = threading.Thread(target=self.__sniff_packet, args=(packet,))
                thread.start()

                # freez main thread to 0.1s
                # to
                time.sleep(0.1)

                # send packet
                scapy.send(packet)
                thread.join()
            else:
                print "User {} not response (ip: {})".format(self.__addressant_name,
                                                             self.__addressant_ip)
