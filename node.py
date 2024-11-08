from strategy import Strategy
from packet import Packet

class Node:
    def __init__(self, location, id, strategy):
        self.location = location
        self.id = id
        self.strategy = strategy

        self.network = None
        self.inbox = []
        self.received_packet_count = 0
        self.sent_packet_count = 0
        self.completed = False

    def set_network(self, network):
        self.network = network
        self.strategy.set_network(network, self)

    def receive_packet(self, packet):
        self.inbox.append(packet)
        self.received_packet_count += 1

    def send_start_packet(self):
        for recipient in self.strategy.get_forwarding_list(None, 0):
            self.network.send(Packet(self, recipient, "start"))

    def handle_packet(self, packet):
        if not self.completed:
            self.completed = True
            for recipient in self.strategy.get_forwarding_list(packet.sender, 0):
                self.network.send(Packet(self, recipient, packet.data))

    def tick(self):
        if self.inbox:
            packet = self.inbox.pop(0)
            self.handle_packet(packet)
