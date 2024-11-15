from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, set_ev_cls
from ryu.lib.packet import ether_types, ethernet, ip
from ryu.ofproto import ofproto_v1_3
from ryu.ofproto.ofproto_v1_3 import OFPActionOutput, OFPMatch, OFPFlowMod, OFPPACKET_OUT
import random

class LeastConnectionsController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(LeastConnectionsController, self).__init__(*args, **kwargs)
        self.switches = {}  # Dictionary to store switch data
        self.connections = {}  # Dictionary to store connections count for each server

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, MAIN_DISPATCHER)
    def switch_features_handler(self, ev):
        # Handler to process switch features, and install a default flow for each switch
        datapath = ev.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Install a default flow rule to handle packet-in
        match = parser.OFPMatch()
        actions = [OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match,
            instructions=inst, buffer_id=buffer_id
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        datapath = ev.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = ev.port
        pkt = ev.msg.data
        pkt_eth = ethernet.ethernet(pkt)

        # Handle IP packets and select the least connected server
        if pkt_eth.ethertype == ether_types.ETH_TYPE_IP:
            pkt_ip = pkt_eth.payload
            src_ip = pkt_ip.src
            dst_ip = pkt_ip.dst

            # Here we assume servers have IPs in a given range
            if dst_ip in self.connections:
                # Find server with least connections
                least_connected_server = min(self.connections, key=self.connections.get)
                self.connections[least_connected_server] += 1  # Increase the connection count
                self.send_packet(datapath, in_port, least_connected_server)

            else:
                self.connections[dst_ip] = 1  # Initialize connection count for new server
                self.send_packet(datapath, in_port, dst_ip)

    def send_packet(self, datapath, in_port, dst_ip):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        actions = [OFPActionOutput(in_port)]
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IP, ipv4_dst=dst_ip)
        self.add_flow(datapath, 1, match, actions)

        # Send packet-out message
        out = parser.OFPPacketOut(datapath=datapath, in_port=in_port, actions=actions)
        datapath.send_msg(out)
