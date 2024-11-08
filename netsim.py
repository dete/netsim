from network import Network
from latency import LatencyModel
from latency_data import latency_data
from node import Node
from gossip import *

import random

def run_simulation(network, start_node_id):
    start_node = network.node_list[start_node_id]
    start_node.send_start_packet()
    total_nodes = len(network.node_list)
    completion_time = None
    completed_nodes = 0

    while network.is_active():
        network.tick()
        completed_nodes = sum(1 for node in network.node_list if node.completed)
        if completion_time is None and completed_nodes == total_nodes:
            completion_time = network.tick_count

        # if network.tick_count % 1000 == 0:
        #     print(f" {network.tick_count/1000}s: {completed_nodes}/{total_nodes} {len(network.in_flight)}/{network.total_packets}")

    if completion_time is not None:
        print(f" Completion time: {completion_time/1000}s")
    else:
        print(f" Completed nodes: {completed_nodes}/{total_nodes}")

    print(f" Total time: {network.tick_count/1000}s")
    print(f" Total packets: {network.total_packets} ({network.total_packets/total_nodes:.3g}x)")

if __name__ == "__main__":
    lat = LatencyModel(latency_data, provider_list=["AWS", "Azure", "Google"],
                       cross_provider_latency_multiplier=3)

    node_count = 100
    degree = 10
    locations = random.choices(lat.locations, k=node_count)

    greedyNodes = [Node(locations[i], i, GreedyGossipStrategy(degree)) for i in range(node_count)]
    greedyNetwork = Network(greedyNodes, lat)
    greedyNetwork.initialize()

    print("Greedy")
    run_simulation(greedyNetwork, 0)

    randomNodes = [Node(locations[i], i, RandomGossipStrategy(degree)) for i in range(node_count)]
    randomNetwork = Network(randomNodes, lat)
    randomNetwork.initialize()

    print("Random")
    run_simulation(randomNetwork, 0)

    halfNodes = [Node(locations[i], i, HalfGreedyGossipStrategy(degree)) for i in range(node_count)]
    halfNetwork = Network(halfNodes, lat)
    halfNetwork.initialize()

    print("Half")
    run_simulation(halfNetwork, 0)
