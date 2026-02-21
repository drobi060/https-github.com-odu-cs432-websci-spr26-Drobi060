#!/usr/bin/env python3
"""
Analyze the directed graph from Q1 and classify nodes according to bow-tie structure
"""

# Define the edges
edges = [
    ('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'D'), ('C', 'G'),
    ('D', 'A'), ('D', 'H'), ('E', 'F'), ('E', 'O'), ('F', 'G'),
    ('G', 'C'), ('H', 'L'), ('J', 'N'), ('K', 'I'), ('M', 'A'),
    ('N', 'L'), ('O', 'J'),
]

# Build adjacency lists
from collections import defaultdict, deque

graph = defaultdict(set)
reverse_graph = defaultdict(set)
all_nodes = set()

for src, dst in edges:
    graph[src].add(dst)
    reverse_graph[dst].add(src)
    all_nodes.add(src)
    all_nodes.add(dst)

# Find strongly connected components using Kosaraju's algorithm
def kosaraju_scc():
    visited = set()
    stack = []
    
    # First DFS to fill stack
    def dfs1(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs1(neighbor)
        stack.append(node)
    
    for node in all_nodes:
        if node not in visited:
            dfs1(node)
    
    # Second DFS on reverse graph
    visited = set()
    sccs = []
    
    def dfs2(node, component):
        visited.add(node)
        component.add(node)
        for neighbor in reverse_graph[node]:
            if neighbor not in visited:
                dfs2(neighbor, component)
    
    while stack:
        node = stack.pop()
        if node not in visited:
            component = set()
            dfs2(node, component)
            sccs.append(component)
    
    return sccs

# Get SCCs
sccs = kosaraju_scc()
print("SCCs found:")
for i, scc in enumerate(sccs):
    print(f"  SCC {i+1}: {sorted(scc)}")

# Find the main SCC (largest one)
main_scc = max(sccs, key=len) if sccs else set()
print(f"\nMain SCC (largest): {sorted(main_scc)}")

# Classify nodes
scc_nodes = main_scc
in_nodes = set()
out_nodes = set()
tendril_nodes = set()
tube_nodes = set()
disconnected_nodes = set()

# IN nodes: can reach SCC but are not in SCC
# OUT nodes: can be reached from SCC but are not in SCC
# Tendrils: can reach OUT or be reached from IN but not in either
# Tubes: part of path between IN and OUT

for node in all_nodes:
    if node in scc_nodes:
        continue
    
    # Check if node can reach SCC
    def can_reach(start, target_set):
        visited = set()
        queue = deque([start])
        visited.add(start)
        while queue:
            current = queue.popleft()
            if current in target_set:
                return True
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
    
    # Check if SCC can reach node
    def can_reach_from_scc(target):
        visited = set()
        queue = deque(scc_nodes)
        visited.update(scc_nodes)
        while queue:
            current = queue.popleft()
            if current == target:
                return True
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return False
    
    can_reach_scc = can_reach(node, scc_nodes)
    scc_can_reach = can_reach_from_scc(node)
    
    if can_reach_scc and not scc_can_reach:
        in_nodes.add(node)
    elif scc_can_reach and not can_reach_scc:
        out_nodes.add(node)
    elif can_reach_scc and scc_can_reach:
        tube_nodes.add(node)
    else:
        # Check if it's a tendril
        can_reach_out = any(can_reach(node, {n}) for n in out_nodes) if out_nodes else False
        can_be_reached_from_in = any(can_reach(n, {node}) for n in in_nodes) if in_nodes else False
        
        if can_reach_out or can_be_reached_from_in:
            tendril_nodes.add(node)
        else:
            disconnected_nodes.add(node)

print(f"\n--- Node Classification ---")
print(f"SCC: {sorted(scc_nodes)}")
print(f"IN: {sorted(in_nodes)}")
print(f"OUT: {sorted(out_nodes)}")
print(f"Tendrils: {sorted(tendril_nodes)}")
print(f"Tubes: {sorted(tube_nodes)}")
print(f"Disconnected: {sorted(disconnected_nodes)}")

# Analyze tendrils more carefully
print(f"\n--- Tendril Analysis ---")
for node in sorted(tendril_nodes):
    can_reach_out = any(can_reach(node, {n}) for n in out_nodes) if out_nodes else False
    can_be_reached_from_in = any(can_reach(n, {node}) for n in in_nodes) if in_nodes else False
    
    reachability = []
    if can_be_reached_from_in:
        reachability.append("reachable from IN")
    if can_reach_out:
        reachability.append("can reach OUT")
    
    print(f"  {node}: {', '.join(reachability)}")

# Export edges for graphviz
print("\n--- Graphviz DOT format ---")
print("digraph G {")
for src, dst in edges:
    print(f"  {src} -> {dst};")
print("}")
