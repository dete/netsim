
from strategy import Strategy
import random
import math

big_prime1 = 0x7FFFFFFF
big_prime2 = 87178291199

class HamiltonionStrategy(Strategy):
    def __init__(self, degree=4):
        super().__init__()
        self.degree = degree
        self.neighbors = []

    def set_network(self, network, node_id):
        super().set_network(network, node_id)

        def gcd(a, b):
            """Calculate the Greatest Common Divisor of a and b using Euclidean algorithm."""
            while b:
                a, b = b, a % b
            return a
        
        hamiltonian_count = math.ceil(self.degree / 2)
        node_count = len(self.network.node_list)
        cycle_strides = []
        backup_strides = []
        i = 1
        max_stride = node_count // 2
        cp1 = big_prime1 % max_stride
        cp2 = big_prime2 % max_stride

        if abs(cp1 - (max_stride//2)) < abs(cp2 - (max_stride//2)):
            stride_stride = cp1
        else:
            stride_stride = cp2

        # Add stride lengths until we have enough to reach our target degree, or run
        # out of numbers less than n/2. (Values above n/2 are equivalent to values
        # below n/2, just in the other direction.)
        while len(cycle_strides) < hamiltonian_count and i < max_stride:
            possible_stride = (i * stride_stride) % max_stride
            gcd_result = gcd(possible_stride, node_count)
            if gcd_result == 1:
                cycle_strides.append(possible_stride)
            elif gcd_result == 2:
                backup_strides.append(possible_stride)
            i += 1
        
        if len(cycle_strides) < hamiltonian_count:
            cycle_strides.extend(backup_strides[:hamiltonian_count - len(cycle_strides)])

        # In the real code, we wouldn't recompute the neighbors here, we would just
        # use cycle_strides to compute the neighbors in the forward list.
        self.neighbors = [self.network.node_list[(self.node.id + stride) % node_count] for stride in cycle_strides]
        self.neighbors.extend([self.network.node_list[(self.node.id + node_count - stride) % node_count] for stride in cycle_strides])

    def get_forward_list(self, sender, codeword_id):
        if sender is None:
            return self.neighbors
        else:
            return [n for n in self.neighbors if n != sender]

if __name__ == "__main__":
    from network import Network
    from latency import LatencyModel
    from node import Node
    from latency_data import latency_data

    lat = LatencyModel(latency_data, provider_list=["AWS", "Azure", "Google"])
    locations = random.sample(lat.locations, 20)

    def print_neighbors(network):
        for node in network.node_list:
            print(f"{node.id} - {node.location} neighbors:", [n.id for n in node.strategy.neighbors], end=" ")
            print(f"Latencies: {[lat.get_latency(node.location, n.location) for n in node.strategy.neighbors]}")
            assert len(node.strategy.neighbors) == 6, "Should have exactly 3 neighbors"
            assert node not in node.strategy.neighbors, "Node shouldn't be its own neighbor"

    hamiltonianNodes = [Node(locations[i], i, HamiltonionStrategy(6)) for i in range(20)]
    hamiltonianNetwork = Network(hamiltonianNodes, lat)
    hamiltonianNetwork.initialize()
    print("Hamiltonion")
    print_neighbors(hamiltonianNetwork)
