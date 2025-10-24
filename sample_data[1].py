# sample_data.py
"""
Sample graph data for Smart Traffic Flow Optimizer.
We provide both edges and optional coordinates for heuristic (A*).
"""

def get_sample_edges():
    """
    Returns list of tuples: (u, v, distance, traffic_factor)
    traffic_factor defaults to 1.0 if normal; >1 means slower (more congestion).
    """
    return [
        ('A', 'B', 4, 1.0),
        ('A', 'C', 2, 1.2),
        ('B', 'C', 1, 1.0),
        ('B', 'D', 5, 1.1),
        ('C', 'D', 8, 1.0),
        ('C', 'E', 10, 1.3),
        ('D', 'E', 2, 1.0),
        ('D', 'Z', 6, 1.4),
        ('E', 'Z', 3, 1.0)
    ]

def get_sample_coords():
    """
    Optional coordinates (x,y) for nodes - used by A* heuristic.
    Coordinates are arbitrary, just for demonstration.
    """
    return {
        'A': (0, 0),
        'B': (4, 0),
        'C': (1, 2),
        'D': (6, 2),
        'E': (7, 4),
        'Z': (9, 5)
    }
