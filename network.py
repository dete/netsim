import networkx as nx


class Network:
    def __init__(self, node_list, latency_model):
        self.node_list = node_list
        self.latency_model = latency_model
        self.tick_count = 0

        self.latency_graph = None
        self.in_flight = []
        self.total_packets = 0

    def initialize(self):
        for node in self.node_list:
            node.set_network(self)

    def get_latency_graph(self):
        if self.latency_graph == None:
            self.latency_graph = nx.Graph()
            
            # Add all nodes
            for node in self.node_list:
                self.latency_graph.add_node(node.id)
            
            # Add edges between all pairs of nodes with latency as weight
            for i, node1 in enumerate(self.node_list):
                for node2 in self.node_list[i+1:]:
                    latency = self.latency_model.get_latency(node1.location, node2.location)
                    self.latency_graph.add_edge(node1.id, node2.id, weight=latency)

        return self.latency_graph

    def send(self, packet):
        packet.source.sent_packet_count += 1
        self.total_packets += 1

        if self.latency_model.has_loss:
            loss_ratio = self.latency_model.get_loss_ratio(packet.source.location,
                packet.destination.location)
            
            # TODO: Compute losses

        # Compute the arrival time of the packet using the latency model
        latency = self.latency_model.get_latency(packet.source.location, packet.destination.location)
        arrival_tick = self.tick_count + latency

        # find the index to insert this new packet so in-flight list is sorted
        left, right = 0, len(self.in_flight)
        while left < right:
            mid = (left + right) // 2
            if self.in_flight[mid][0] > arrival_tick:
                left = mid + 1
            else:
                right = mid

        # insert the packet to be picked up later
        self.in_flight.insert(left, (arrival_tick, packet))

    def tick(self):
        self.tick_count += 1  # Increment tick count

        while self.in_flight and self.in_flight[-1][0] <= self.tick_count:
            _, packet = self.in_flight.pop()
            packet.destination.receive_packet(packet)
        
        for node in self.node_list:
            node.tick()

    def is_active(self):
        # Check if there are any codewords in transit
        if self.in_flight:
            return True

        # Check if there are any codewords in any node's inbox
        for node in self.node_list:
            if node.inbox:
                return True

        return False

    def __repr__(self):
        return (f"Network(ticks={self.tick_count}, "
                f"in-flight={len(self.in_flight)}, "
#                f"recipients_completed={[recipient.completed for recipient in self.recipients]}, "
                f"total_codewords={self.total_codewords})")

