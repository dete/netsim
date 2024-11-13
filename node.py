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
        self.first_packet_tick = None
        self.remaining_recipients = set()

    def set_network(self, network):
        self.network = network
        self.strategy.set_network(network, self)
        self.remaining_recipients = list(self.strategy.get_forward_list(None, 0))

    def receive_packet(self, packet):
        self.inbox.append(packet)
        self.received_packet_count += 1

    def send_to_random_recipient(self):
        recipient = self.remaining_recipients.pop()
        self.sent_packet_count += 1
        self.network.send(Packet(self, recipient, "start"))
        if not self.remaining_recipients:
            self.completed = True

    def send_start_packet(self):
        while self.remaining_recipients:
            self.send_to_random_recipient()
        self.completed = True

    def handle_packet(self, packet):
        if packet.source in self.remaining_recipients:
            self.remaining_recipients.remove(packet.source)
        if not self.remaining_recipients:
            self.completed = True
        elif self.sent_packet_count == 0:
            # Send packets to two random recipients
            self.send_to_random_recipient()
            self.send_to_random_recipient()

    def tick(self):
        while self.inbox:
            if self.first_packet_tick == None:
                self.first_packet_tick = self.network.tick_count
            packet = self.inbox.pop(0)
            self.handle_packet(packet)

        while self.first_packet_tick and self.remaining_recipients:# and self.network.tick_count - self.first_packet_tick > 100:
            self.send_to_random_recipient()
