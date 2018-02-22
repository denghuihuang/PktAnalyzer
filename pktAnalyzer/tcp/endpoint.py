from packet import Packet
from dpkt.tcp import TH_SYN
from flow import NewFlowError


RECEIVE_DIR = 0
SENDER_DIR = 1

class EndPoint(object):
    '''
    Represents TCP traffic across a given socket, ideally between a TCP
    handshake and clean connection termination.

    Members:
    * fwd = this ip address of this endpoint
    * port = this tcp port listening by this endpoint
    * unack_send_packets = packets sent by this endpoint, but not acknowledging by peer
    * unack_recv_packets = packets receiving from peer, but acknowledged yet
    * formats:
    *         [(pkt.seq,pkt.len,pkt)]-
    '''
    def __init__(self, IP, port):
        self.IP = IP
        self.port = port
        self.unack_send_packets = []
        self.unack_recv_packets = []
        self.retransmited_packets = []
        self.duplicated_packets = []
        self.state = None

    def add(self, pkt):
        '''

        Args:
            pkt:

        Returns:

        '''
        seq = pkt.tcp.seq
        if (self.IP, self.port) == (pkt.ip.dst, pkt.tcp.dport):
            #recv packet
            #state transfer
            self.state_transfer(pkt)

            self.is_duplicated_packet(pkt, RECEIVE_DIR)

            self.is_retransmited_packet(pkt, RECEIVE_DIR)

            pkt_info = (pkt.seq_start, pkt.seq_end, pkt)
            self.unack_recv_packets.append(pkt_info)

        else:
            #send packet
            pass


    def valid_packet(self, pkt):
        '''
        valid this packet
        Args:
            pkt:

        Returns:
            true, if it is a valid packet
            false, if it is a invalid packet
        '''
        pass

    def is_duplicated_packet(self, pkt, direction):
        '''
        whether it is duplicated packet
        Args:
            pkt: packet
            direction: receive or send
        Returns:
            true, if it is a duplicated packet
            false, if it is not a duplicated packet
        '''
        if direction == RECEIVE_DIR:
            for pkt_info in self.unack_recv_packets:
                seq, end, pkt = pkt_info
                if (pkt.seq, pkt.seq_end) == (seq, end):
                    pass


        else:
            for pkt_info in self.unack_send_packets:
                pass
            pass
        pass

    def is_out_of_order_packet(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def is_retransmited_packet(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_transfer(self, pkt):
        '''

        Args:
            pkt:

        Returns:

        '''
        pass
