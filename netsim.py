

def run_simulation(network, start_node_id):
    start_node = network.node_list[start_node_id]
    start_node.send_start_packet()

    while network.is_active():
        network.tick()

        if network.tick_count % 100 == 0:
            completed_nodes = sum(1 for node in network.node_list if node.completed)
            print(f"{network.tick_count/1000}s: {completed_nodes}/{len(network.node_list)} {len(network.)}")
