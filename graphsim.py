import networkx as nx
import sympy as sp
from sympy.logic.boolalg import Or, And
from itertools import combinations
import math
import random

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
    max_val = values[-1]
    
    # Generate a target geometric series
    base = max_val ** (1 / (k - 1))
    targets = [(base ** i) for i in range(k)]

    print(f"Base: {base}")
    print(f"Targets: {targets}")
    
    # Select closest values from the list
    selected_values = []
    remaining_values = values[:]
    for target in targets:
        # Find the closest value in the remaining list
        closest = min(remaining_values, key=lambda v: abs(v - target))
        selected_values.append(closest)
        remaining_values.remove(closest)  # Avoid duplicates
    
    print(f"Selected values: {selected_values}")
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

def add_hamiltonian_cycles(G, k):
    n = G.number_of_nodes()
    cp = get_coprimes(n)
    cycles = select_geometric_series(cp, math.ceil(k/2))
    for i in range(n):
        for c in cycles:
            s = i*c % n
            t = (i + 1)*c % n
            G.add_edge(s, t)

def add_random_edges(G, k):
    n = G.number_of_nodes()
    for node in range(n):
        for edge in range(math.ceil(k/2)):
            target = random.randint(0, n - 2)
            if target >= node:
                target += 1
            G.add_edge(node, target)

def add_tree_edges(G, k):
    n = G.number_of_nodes()
    total_messages = n * k
    fanout = math.ceil(math.sqrt(total_messages))
    print(f"Fanout: {fanout}")
    cycles = get_coprimes(n)
    if len(cycles) > k:
        cycles = select_geometric_series(cycles, k)
    elif len(cycles) < k:
        cycles = random.choices(cycles, k=k)

    print(f"Cycles: {cycles}")

    for c in cycles:
        for i in range(math.ceil(fanout/k)):
            target = ((i * fanout + 1) * c) % n
            G.add_edge(0, target)
            for j in range(1, fanout):
                secondary = ((i * fanout + j + 1) * c) % n
                G.add_edge(target, secondary)

n = 1000
G = nx.Graph()
G.add_nodes_from(range(n))
symbols = sp.symbols([f"P{i}" for i in range(n)])
amp = 8

add_hamiltonian_cycles(G, amp)
# add_random_edges(G, amp)
# add_tree_edges(G, amp)

# print(G.edges())

print(f"Degree range: {min([d for n, d in G.degree()])} - {max([d for n, d in G.degree()])}")
print(f"Diameter: {nx.diameter(G)}")
print(f"Eccentricity: {nx.eccentricity(G, v=0)}")


testing_combos = []
combo_count = math.comb(n, n // 3)
sample_size = 10000

if combo_count < sample_size:
    print("Testing all combos")
    testing_combos = combinations(range(n), n // 3)
elif combo_count < sample_size * 10:
    print("Testing with reservoir sampling")
    testing_combos = reservoir_sampling_combinations(combinations(range(n), n // 3), sample_size)
else:
    print("Testing with random sampling")
    random_set = set()
    while len(random_set) < sample_size:
        candidate = random.sample(range(n), n // 3)
        candidate.sort()
        random_set.add(tuple(candidate))
    testing_combos = list(random_set)

success_count = 0
total_count = 0

for combo in testing_combos:
    test = G.copy()
    test.remove_nodes_from(combo)
    total_count += 1
    if nx.is_connected(test):
        success_count += 1

print(success_count / total_count)
