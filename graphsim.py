import networkx as nx
import sympy as sp
from sympy.logic.boolalg import Or, And
from itertools import combinations
import math

def get_coprimes(n, count):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    coprimes = []
    num = 1
    while len(coprimes) < count:
        if gcd(num, n) == 1:
            coprimes.append(num)
        num += 1
    return coprimes


n = 21
G = nx.Graph(nodes=range(n))
cycles = get_coprimes(n, 2)
symbols = sp.symbols([f"P{i}" for i in range(n)])
# print(cycles)

for i in range(n):
    for c in cycles:
        s = i*c % n
        t = (i + 1)*c % n
        G.add_edge(s, t)

edge_paths = nx.all_simple_edge_paths(G, 0, 4)
expression = sp.Or()

for path in edge_paths:
    sub_expression = sp.And()
    for s, t in path:
        sub_expression &= symbols[s]
    expression |= sub_expression

#expression = sp.simplify(expression)

all_good = {symbols[i]: True for i in range(n)}

testing_combos = combinations(all_good, n // 3)
combo_count = math.comb(n, n // 3)

if combo_count > 1000:
    print("Too many combos")
    exit()

success_count = 0
total_count = 0

for combo in testing_combos:
    test = all_good.copy()
    for i in combo:
        test[i] = False
    total_count += 1
    if expression.subs(test):
        success_count += 1

print(success_count / total_count)
