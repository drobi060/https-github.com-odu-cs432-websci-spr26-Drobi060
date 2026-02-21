#!/usr/bin/env python3
"""
Create a visual graph diagram for Q1
"""

import os
try:
    import matplotlib.pyplot as plt
    import networkx as nx
except ImportError:
    print("Installing required packages...")
    os.system("pip install matplotlib networkx -q")
    import matplotlib.pyplot as plt
    import networkx as nx

# Define edges
edges = [
    ('A', 'B'), ('B', 'A'), ('B', 'C'), ('C', 'D'), ('C', 'G'),
    ('D', 'A'), ('D', 'H'), ('E', 'F'), ('E', 'O'), ('F', 'G'),
    ('G', 'C'), ('H', 'L'), ('J', 'N'), ('K', 'I'), ('M', 'A'),
    ('N', 'L'), ('O', 'J'),
]

# Create directed graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Node classification
scc_nodes = {'A', 'B', 'C', 'D', 'G'}
in_nodes = {'E', 'F', 'M'}
out_nodes = {'H', 'L'}
tendril_nodes = {'N', 'O', 'J'}
disconnected_nodes = {'I', 'K'}

# Create colors for nodes
node_colors = []
color_map = {
    'scc': '#FF6B6B',      # Red
    'in': '#4ECDC4',       # Teal
    'out': '#45B7D1',      # Blue
    'tendril': '#FFA07A',  # Light Salmon
    'disconnected': '#95A5A6'  # Gray
}

for node in G.nodes():
    if node in scc_nodes:
        node_colors.append(color_map['scc'])
    elif node in in_nodes:
        node_colors.append(color_map['in'])
    elif node in out_nodes:
        node_colors.append(color_map['out'])
    elif node in tendril_nodes:
        node_colors.append(color_map['tendril'])
    else:
        node_colors.append(color_map['disconnected'])

# Create figure
plt.figure(figsize=(14, 10))

# Use spring layout for better visualization
pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

# Draw the graph
nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1500, alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                       arrowsize=20, arrowstyle='->', 
                       connectionstyle='arc3,rad=0.1', width=2)

# Create legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor=color_map['scc'], edgecolor='black', label='SCC (Core): A, B, C, D, G'),
    Patch(facecolor=color_map['in'], edgecolor='black', label='IN: E, F, M'),
    Patch(facecolor=color_map['out'], edgecolor='black', label='OUT: H, L'),
    Patch(facecolor=color_map['tendril'], edgecolor='black', label='Tendrils: J, N, O'),
    Patch(facecolor=color_map['disconnected'], edgecolor='black', label='Disconnected: I, K'),
]
plt.legend(handles=legend_elements, loc='upper left', fontsize=10)

plt.title('Q1: Directed Graph Analysis - Bow-Tie Structure', fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.savefig('/workspaces/https-github.com-odu-cs432-websci-spr26-Drobi060/q1_graph.png', dpi=300, bbox_inches='tight')
print("Graph saved to q1_graph.png")
plt.close()

# Also create a more structured layout
fig, ax = plt.subplots(figsize=(16, 10))

# Manual positioning for bow-tie structure
pos_manual = {
    # IN nodes on the left
    'E': (0, 1),
    'F': (0, 0),
    'M': (0, -1),
    
    # SCC in the middle
    'A': (2, 0.5),
    'B': (2, 1.5),
    'C': (2.5, 0),
    'D': (2, -0.5),
    'G': (3, 0),
    
    # OUT nodes on the right
    'H': (4, 0.5),
    'L': (4, -0.5),
    
    # Tendrils
    'O': (1, 0),
    'J': (2.5, -1.5),
    'N': (3.5, -1.5),
    
    # Disconnected
    'I': (0.5, -2),
    'K': (0.5, -2.5),
}

nx.draw_networkx_nodes(G, pos_manual, node_color=node_colors, node_size=2000, alpha=0.9)
nx.draw_networkx_labels(G, pos_manual, font_size=11, font_weight='bold')
nx.draw_networkx_edges(G, pos_manual, edge_color='gray', arrows=True, 
                       arrowsize=25, arrowstyle='->', 
                       connectionstyle='arc3,rad=0.1', width=2.5)

plt.legend(handles=legend_elements, loc='upper left', fontsize=11)
plt.title('Q1: Directed Graph - Bow-Tie Structure (Structured Layout)', fontsize=14, fontweight='bold')
ax.set_xlim(-1, 5)
ax.set_ylim(-3, 2.5)
plt.axis('off')
plt.tight_layout()
plt.savefig('/workspaces/https-github.com-odu-cs432-websci-spr26-Drobi060/q1_graph_structured.png', dpi=300, bbox_inches='tight')
print("Structured graph saved to q1_graph_structured.png")
