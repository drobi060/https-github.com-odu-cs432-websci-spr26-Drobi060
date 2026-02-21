#!/usr/bin/env python3
"""
More detailed analysis of the bow-tie structure
"""

from collections import defaultdict, deque

edges = [
    ('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'D'), ('C', 'G'),
    ('D', 'A'), ('D', 'H'), ('E', 'F'), ('E', 'O'), ('F', 'G'),
    ('G', 'C'), ('H', 'L'), ('J', 'N'), ('K', 'I'), ('M', 'A'),
    ('N', 'L'), ('O', 'J'),
]

graph = defaultdict(set)
reverse_graph = defaultdict(set)
all_nodes = set()

for src, dst in edges:
    graph[src].add(dst)
    reverse_graph[dst].add(src)
    all_nodes.add(src)
    all_nodes.add(dst)

# Can reach helper
def can_reach(start, target, graph_dict):
    if start == target:
        return True
    visited = set()
    queue = deque([start])
    visited.add(start)
    while queue:
        current = queue.popleft()
        for neighbor in graph_dict[current]:
            if neighbor == target:
                return True
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return False

# Main SCC
main_scc = {'A', 'B', 'C', 'D', 'G'}
in_nodes = {'E', 'F', 'M'}
out_nodes = {'H', 'L'}

# Analyze N
print("Analyzing N:")
print(f"  N can reach H? {can_reach('N', 'H', graph)}")
print(f"  N can reach L? {can_reach('N', 'L', graph)}")
print(f"  E can reach N? {can_reach('E', 'N', graph)}")
print(f"  F can reach N? {can_reach('F', 'N', graph)}")
print(f"  M can reach N? {can_reach('M', 'N', graph)}")

print("\nAnalyzing O:")
print(f"  O can reach H? {can_reach('O', 'H', graph)}")
print(f"  O can reach L? {can_reach('O', 'L', graph)}")
print(f"  E can reach O? {can_reach('E', 'O', graph)}")
print(f"  F can reach O? {can_reach('F', 'O', graph)}")
print(f"  M can reach O? {can_reach('M', 'O', graph)}")

print("\nAnalyzing I, J, K:")
print(f"  K in graph nodes? {can_reach('K', 'I', graph)}")
print(f"  J in graph nodes? {can_reach('J', 'N', graph)}")
print(f"  I connections: in={list(reverse_graph['I'])}, out={list(graph['I'])}")
print(f"  J connections: in={list(reverse_graph['J'])}, out={list(graph['J'])}")
print(f"  K connections: in={list(reverse_graph['K'])}, out={list(graph['K'])}")

# For tubes: nodes that connect IN to OUT but are not in SCC
print("\n--- Checking for Tube nodes (path from IN to OUT) ---")
for node in all_nodes:
    if node in main_scc or node in in_nodes or node in out_nodes:
        continue
    # Check if node lies on path from any IN to any OUT
    is_tube = False
    for in_node in in_nodes:
        for out_node in out_nodes:
            if can_reach(in_node, node, graph) and can_reach(node, out_node, graph):
                print(f"{node}: connects {in_node} -> {out_node}")
                is_tube = True
    
    if not is_tube:
        print(f"{node}: NOT a tube")
