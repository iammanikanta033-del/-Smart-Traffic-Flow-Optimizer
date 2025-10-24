# main.py
"""
Interactive command-line interface to run Smart Traffic Flow Optimizer.
This enhanced version includes optional visualization using networkx + matplotlib.
Visualization is optional and will be attempted only if the libraries are installed.
"""

import csv
import sys
from graph import Graph
from sample_data import get_sample_edges, get_sample_coords

try:
    import networkx as nx
    import matplotlib.pyplot as plt
    VIS_AVAILABLE = True
except Exception:
    VIS_AVAILABLE = False

def load_graph_from_csv(path: str) -> Graph:
    g = Graph()
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row['u'].strip()
            v = row['v'].strip()
            d = float(row['distance'])
            t = float(row.get('traffic_factor', 1.0))
            g.add_edge(u, v, d, t, bidirectional=True)
    return g

def visualize_graph(g: Graph, path=None, title="Smart Traffic Flow Optimizer"):
    if not VIS_AVAILABLE:
        print("Visualization libraries not installed. Install with: pip install networkx matplotlib")
        return
    G = nx.Graph()
    for node in g.nodes():
        G.add_node(node)
    for u, v, d, t in g.edges():
        G.add_edge(u, v, weight=round(d * t,2))
    pos = {}
    if g.coords:
        pos = {n: g.coords[n] for n in g.coords}
    else:
        pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    if path:
        # highlight path edges
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3.0, edge_color='r')
    plt.title(title)
    plt.tight_layout()
    plt.show()

def interactive():
    print("=== Smart Traffic Flow Optimizer ===")
    g = Graph()
    last_result = None

    while True:
        print("\nMenu:")
        print("1) Load sample graph")
        print("2) Load graph from CSV file")
        print("3) Add edge manually")
        print("4) Show nodes and edges")
        print("5) Find shortest path (Dijkstra)")
        print("6) Find shortest path (A*)")
        print("7) Visualize graph (optional)")
        print("8) Save last result to file")
        print("0) Exit")

        choice = input("Choose option: ").strip()
        if choice == '1':
            edges = get_sample_edges()
            coords = get_sample_coords()
            g = Graph()
            for u, v, d, t in edges:
                g.add_edge(u, v, d, t, bidirectional=True)
            for node, coord in coords.items():
                g.add_node(node, coord=coord)
            print("Sample graph loaded.")
        elif choice == '2':
            path = input("Enter CSV file path: ").strip()
            try:
                g = load_graph_from_csv(path)
                print("Graph loaded from CSV.")
            except Exception as e:
                print("Failed to load CSV:", e)
        elif choice == '3':
            try:
                u = input("From node: ").strip()
                v = input("To node: ").strip()
                d = float(input("Distance (number): ").strip())
                t = input("Traffic factor (default 1.0): ").strip()
                t = float(t) if t else 1.0
                g.add_edge(u, v, d, t, bidirectional=True)
                print(f"Added edge {u} <-> {v} (d={d}, t={t})")
            except Exception as e:
                print("Invalid input:", e)
        elif choice == '4':
            print("Nodes:", g.nodes())
            print("Edges:")
            for u, v, d, t in g.edges():
                print(f"  {u} -> {v} : dist={d}, traffic={t}")
        elif choice == '5' or choice == '6':
            algo = 'Dijkstra' if choice == '5' else 'A*'
            start = input("Start node: ").strip()
            end = input("End node: ").strip()
            if start not in g.adj or end not in g.adj:
                print("Start or end node not in graph. Load data or add nodes/edges first.")
                continue
            try:
                if algo == 'Dijkstra':
                    path, total = g.shortest_path_dijkstra(start, end)
                else:
                    path, total = g.a_star(start, end)
                if not path:
                    print(f"No path found from {start} to {end}.")
                    last_result = None
                else:
                    print(f"{algo} path: {' -> '.join(path)}")
                    print(f"Total effective distance (considering traffic): {total:.3f}")
                    last_result = {
                        'algorithm': algo,
                        'start': start,
                        'end': end,
                        'path': path,
                        'total': total
                    }
                    viz = input("Visualize this path? (y/N): ").strip().lower()
                    if viz == 'y':
                        visualize_graph(g, path=path, title=f\"{algo} Path: {start} -> {end}\")
            except Exception as e:
                print("Error running algorithm:", e)
        elif choice == '7':
            visualize_graph(g)
        elif choice == '8':
            if not last_result:
                print("No result to save. Run a path search first.")
                continue
            fname = input("Enter file name to save (e.g. route_result.txt): ").strip()
            try:
                with open(fname, 'w') as f:
                    f.write(f"Algorithm: {last_result['algorithm']}\n")
                    f.write(f"Start: {last_result['start']}\n")
                    f.write(f"End: {last_result['end']}\n")
                    f.write("Path: " + " -> ".join(last_result['path']) + "\n")
                    f.write(f"Total effective distance: {last_result['total']:.3f}\n")
                print("Saved to", fname)
            except Exception as e:
                print("Failed to save:", e)
        elif choice == '0':
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # quick demo run using sample data (non-interactive) + auto-visualize if available
        g = Graph()
        for u, v, d, t in get_sample_edges():
            g.add_edge(u, v, d, t, bidirectional=True)
        for node, coord in get_sample_coords().items():
            g.add_node(node, coord=coord)
        s, e = 'A', 'Z'
        path_dij, tot_dij = g.shortest_path_dijkstra(s, e)
        path_ast, tot_ast = g.a_star(s, e)
        print("Dijkstra:", " -> ".join(path_dij), tot_dij)
        print("A*     :", " -> ".join(path_ast), tot_ast)
        # auto-visualize
        visualize_graph(g, path=path_dij, title=\"Dijkstra Demo Path: A -> Z\")
    else:
        interactive()
