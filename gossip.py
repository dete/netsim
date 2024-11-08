from strategy import Strategy
import random
import math

class GossipStrategy(Strategy):
    def __init__(self, degree=4):
        super().__init__()
        self.degree = degree
        self.neighbors = []

    def add_closest_neighbors(self, count):
        possible_neighbors = [n for n in self.network.node_list if n != self.node and n not in self.neighbors]
        lat = self.network.latency_model

        self.neighbors.extend(sorted(possible_neighbors, key=lambda x: lat.get_latency(self.node.location, x.location))[:count])

    def add_random_neighbors(self, count):
        possible_neighbors = [n for n in self.network.node_list if n != self.node and n not in self.neighbors]
        self.neighbors.extend(random.sample(possible_neighbors, count))

    def set_network(self, network, node_id):
        super().set_network(network, node_id)

    def get_forward_list(self, sender, codeword_id):
        if sender is None:
            return self.neighbors
        else:
            return [n for n in self.neighbors if n != sender]
    

class GreedyGossipStrategy(GossipStrategy):
    def __init__(self, degree=4):
        super().__init__(degree)
    
    def set_network(self, network, node_id):
        super().set_network(network, node_id)
        self.add_closest_neighbors(self.degree)

class RandomGossipStrategy(GossipStrategy):
    def __init__(self, degree=4):
        super().__init__(degree)
    
    def set_network(self, network, node_id):
        super().set_network(network, node_id)
        self.add_random_neighbors(self.degree)

class HalfGreedyGossipStrategy(GossipStrategy):
    def __init__(self, degree=4):
        super().__init__(degree)
    
    def set_network(self, network, node_id):
        super().set_network(network, node_id)
        self.add_closest_neighbors(math.floor(self.degree / 2))
        self.add_random_neighbors(math.ceil(self.degree / 2))

if __name__ == "__main__":
    from network import Network
    from latency import LatencyModel
    from node import Node
    from latency_data import latency_data

    lat = LatencyModel(latency_data, provider_list=["AWS", "Azure", "Google"])
    locations = random.sample(lat.locations, 20)

    def print_neighbors(network):
        for node in greedyNetwork.node_list:
            print(f"{node.id} - {node.location} neighbors:", [n.id for n in node.strategy.neighbors], end=" ")
            print(f"Latencies: {[lat.get_latency(node.location, n.location) for n in node.strategy.neighbors]}")
            assert len(node.strategy.neighbors) == 6, "Should have exactly 3 neighbors"
            assert node not in node.strategy.neighbors, "Node shouldn't be its own neighbor"

    greedyNodes = [Node(locations[i], i, GreedyGossipStrategy(6)) for i in range(20)]
    greedyNetwork = Network(greedyNodes, lat)
    greedyNetwork.initialize()
    print("Greedy")
    print_neighbors(greedyNetwork)

    randomNodes = [Node(locations[i], i, RandomGossipStrategy(6)) for i in range(20)]
    randomNetwork = Network(randomNodes, lat)
    randomNetwork.initialize()
    print("Random")
    print_neighbors(randomNetwork)

    halfNodes = [Node(locations[i], i, HalfGreedyGossipStrategy(6)) for i in range(20)]
    halfNetwork = Network(halfNodes, lat)
    halfNetwork.initialize()
    print("Half")
    print_neighbors(halfNetwork)
