import networkx as nx
from itertools import combinations
import math
import random
import numpy as np

def get_coprimes(n):
    # require n to be larger than 5
    n = int(n)
    if n <= 5:
        raise ValueError("n must be larger than 5")
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    coprimes = [1]
    for num in range(2, n//2):
        if gcd(num, n) == 1:
            coprimes.append(num)

    return coprimes

def select_geometric_series(values, k):
    if k == 1:
        return [values[0]]
    
    if k > len(values):
        raise ValueError(f"k is larger than the number of values: {k} > {len(values)}")
    
    max_val = values[-1]
    
    # Generate a target geometric series
    base = max_val ** (1 / (k - 1))
    targets = [(base ** i) for i in range(k)]

    # print(f"Base: {base}")
    # print(f"Targets: {targets}")
    
    # Select closest values from the list
    selected_values = []
    remaining_values = values[:]
    for target in targets:
        # Find the closest value in the remaining list
        closest = min(remaining_values, key=lambda v: abs(v - target))
        selected_values.append(closest)
        remaining_values.remove(closest)  # Avoid duplicates
    
    # print(f"Selected values: {selected_values}")
    return selected_values

def reservoir_sampling_combinations(iterable, k):
    # Initialize the reservoir with the first k combinations
    reservoir = []
    for idx, combination in enumerate(iterable):
        if idx < k:
            reservoir.append(combination)
        else:
            # Generate a random index to potentially replace in the reservoir
            j = random.randint(0, idx)
            if j < k:
                reservoir[j] = combination

    return reservoir

def hamiltonian_graph(n, k):
    G = nx.DiGraph()
    cp = get_coprimes(n)
    cycles = select_geometric_series(cp, math.ceil(k))
    for c in cycles:
        for i in range(n-1):
            s = i*c % n
            t = (i + 1)*c % n
            G.add_edge(s, t)
    return G

def random_graph(n, k):
    G = nx.DiGraph()
    for node in range(n):
        for edge in range(math.ceil(k)):
            target = random.randint(0, n - 2)
            if target >= node:
                target += 1
            G.add_edge(node, target)
    return G

def tree_graph(n, k):
    G = nx.DiGraph()
    total_messages = n * k
    fanout = math.ceil(math.sqrt(total_messages))
    print(f"Fanout: {fanout}")
    cycles = get_coprimes(n)
    if len(cycles) > k:
        cycles = select_geometric_series(cycles, k)
    elif len(cycles) < k:
        cycles = random.choices(cycles, k=k)

    for c in cycles:
        for i in range(math.ceil(fanout/k)):
            target = ((i * fanout + 1) * c) % n
            G.add_edge(0, target)
            for j in range(1, fanout):
                secondary = ((i * fanout + j + 1) * c) % n
                G.add_edge(target, secondary)
    return G

print("graph_type,n,amp,success_rate,failure_ratio")

for n in [31, 101, 301, 1001, 3001, 10001]:
    for amp in [1]:#2, 4, 8, 12]:
        for graph_type, graph_fn in [
            # ("hamiltonian", hamiltonian_graph),
            # ("random", random_graph), 
            ("tree", tree_graph)
        ]:
            G = graph_fn(n, amp)

            node_degree = [d for n, d in G.degree()]
            # print(f"Degree range: {min(node_degree)} - {max(node_degree)}")
            # print(f"Edges: {G.number_of_edges()}")
            # print(f"Eccentricity: {nx.eccentricity(G, v=0)}")
            
            testing_combos = []
            combo_count = math.comb(n, n // 3)
            sample_size = 10000

            if combo_count < sample_size:
                testing_combos = combinations(range(1, n), n // 3)
            elif combo_count < sample_size * 10:
                testing_combos = reservoir_sampling_combinations(combinations(range(1, n), n // 3), sample_size)
            else:
                random_set = set()
                while len(random_set) < sample_size:
                    candidate = random.sample(range(1, n), n // 3)
                    candidate.sort()
                    random_set.add(tuple(candidate))
                testing_combos = list(random_set)

            success_count = 0
            total_count = 0
            failure_ratios = []

            for combo in testing_combos:
                test = G.copy()
                test.remove_nodes_from(combo)
                total_count += 1
                desc = nx.descendants(test, 0)
                if len(desc) == n - len(combo) - 1:
                    success_count += 1
                else:
                    failure_ratios.append(len(desc) / (n - len(combo)))

            success_rate = success_count / total_count
            print(f"{graph_type},{n},{amp},{success_rate},{len(failure_ratios) and np.mean(failure_ratios) or "nan"}", flush=True)
