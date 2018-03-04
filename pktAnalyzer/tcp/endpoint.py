from packet import Packet
from dpkt.tcp import TH_SYN
from flow import NewFlowError


RECEIVE_DIR = 0
SENDER_DIR = 1
STATE_CLOSE = 0
STATE_SYN_SENT = 1
STATE_SYN_RECV = 2
STATE_ESTABLISHED = 3
STATE_CLOSING_WAITING = 4
STATE_LAST_ACK = 5
STATE_FIN_WAIT1 = 6
STATE_FIN_WAIT2 = 7
STATE_CLOSING = 8
STATE_TIME_WAIT = 9

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
    *         [(pkt.seq,pkt.len,pkt)]
    '''
    def __init__(self, IP, port, side):
        self.IP = IP
        self.port = port
        self.unack_send_packets = []
        self.acked_send_packets = []
        self.unack_recv_packets = []
        self.acked_recv_packets = []
        self.retransmited_packets = []
        self.duplicated_packets = []
        self.side = side
        self.state = STATE_CLOSE
        self.state_handler = {
            STATE_CLOSE: self.state_close_handler,
            STATE_SYN_SENT: self.state_syn_sent_handler,
            STATE_SYN_RECV: self.state_syn_revc_handler,
            STATE_ESTABLISHED: self.state_establish_handler,
            STATE_CLOSING_WAITING: self.state_closing_handler,
            STATE_LAST_ACK: self.state_last_ack_handler,
            STATE_FIN_WAIT1: self.state_fin_wait1_handler,
            STATE_FIN_WAIT2: self.state_fin_wait2_handler,
            STATE_CLOSING: self.state_closing_handler,
            STATE_TIME_WAIT: self.state_time_wait_handler
        }

    def state_syn_recv_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_establish_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_closing_waiting_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_last_ack_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_fin_wait1_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_fin_wait2_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_closing_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_time_wait_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_syn_sent_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def state_close_handler(self, pkt, direction):
        '''

        Args:
            pkt:
            direction:

        Returns:

        '''
        pass

    def add(self, pkt):
        '''

        Args:
            pkt:

        Returns:

        '''
        if (self.IP, self.port) == (pkt.ip.dst, pkt.tcp.dport):
            #recv direction
            direction = RECEIVE_DIR
        else:
            #send packet
            direction = SENDER_DIR

        func = self.state_handler.get(self.state_handler)
        func(pkt, direction)

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
