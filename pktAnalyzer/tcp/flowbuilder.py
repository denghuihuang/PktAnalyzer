import flow as tcp
import logging

ENDPOINT_CLIENT = 0
ENDPOINT_SERVER = 1


class FlowBuilder(object):
    '''
    Builds and stores tcp.Flow's from packets.

    Takes a series of tcp.Packet's and sorts them into the correct tcp.Flow's
    based on their socket. Exposes them in a dictionary keyed by socket. Call
    .add(pkt) for each packet. This will find the right tcp.Flow in the dict and
    call .add() on it. This class should be renamed.

    Members:
    flowdict = {socket: [tcp.Flow]}
    '''

    def  __init__(self):
        self.flowdict = {}

    def add(self, pkt, from_side):
        '''
        filters out unhandled packets, and sorts the remainder into the correct
        flow
        '''
        #shortcut vars
        src, dst = pkt.socket
        srcip, srcport = src
        dstip, dstport = dst

        # sort the packet into a tcp.Flow in flowdict. If NewFlowError is
        # raised, the existing flow doesn't want any more packets, so we
        # should start a new flow.
        if (src, dst) in self.flowdict or (dst, src) in self.flowdict:
            try:
                self.flowdict[(src, dst)][-1].add(pkt)
            except tcp.NewFlowError:
                self.new_flow((src, dst), pkt)
        else:
            self.new_flow((src, dst), pkt)

    def new_flow(self, socket, packet):
        '''
        Adds a new flow to flowdict for socket, and adds the packet.

        Socket must either be present in flowdict or missing entirely, eg., if
        you pass in (src, dst), (dst, src) should not be present.

        Args:
        * socket: ((ip, port), (ip, port))
        * packet: tcp.Packet
        '''
        newflow = tcp.Flow()
        newflow.add(packet)
        if socket in self.flowdict:
            self.flowdict[socket].append(newflow)
        else:
            self.flowdict[socket] = [newflow]

    def flows(self):
        '''
        Generator that iterates over all flows.
        '''
        for flowlist in self.flowdict.itervalues():
            for flow in flowlist:
                yield flow

    def finish(self):
        map(tcp.Flow.finish, self.flows())
