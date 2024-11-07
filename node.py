from strategy import Strategy

class Node:
    def __init__(self, location, id, strategy):
        self.location = location
        self.id = id
        self.inbox = []
        self.received_packet_count = 0
        self.sent_packet_count = 0
        self.strategy = strategy
        self.network = None

    def set_network(self, network):
        self.network = network
        self.strategy.set_network(network, self.id)

    def receive_packet(self, packet):
        self.inbox.append(packet)
        self.received_packet_count += 1

    def tick(self):
        # Define behavior for each tick
        pass
