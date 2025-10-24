# 🚦 Smart Traffic Flow Optimizer  
### *Python | OOP | DSA | Graph Algorithms (Dijkstra & A*)*

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![DSA](https://img.shields.io/badge/Concepts-DSA%20%26%20OOP-green)
![Algorithm](https://img.shields.io/badge/Algorithm-Dijkstra%20%26%20A*-orange)
![Status](https://img.shields.io/badge/Status-Completed-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🧠 Project Overview
**Smart Traffic Flow Optimizer** is a Python-based project that finds the **optimal route between two locations** using **Dijkstra’s Algorithm** and **A*** Search.  

It simulates real-world traffic optimization by considering **congestion (traffic factor)** on roads.  


---

## 🌟 Key Highlights
- 🧩 **OOP Design:** Modular `Graph` and `Edge` classes for clean architecture  
- ⚙️ **Algorithms:** Implements both **Dijkstra** and **A*** pathfinding  
- 🚦 **Traffic Simulation:** Edge weights adapt to congestion via `traffic_factor`  
- 💬 **Interactive CLI:** Add edges, load from CSV, view routes, and save reports  
- 💾 **File I/O:** Load network data from CSV or use preloaded sample data  
- 🧮 **Visualization (optional):** Uses `networkx` + `matplotlib` to plot graphs and highlight the found path
- 🧮 **Pure Python core:** Core DSA logic remains dependency-free

---

## 🧱 Folder Structure
```
SmartTrafficFlowOptimizer/
│
├── graph.py         # Core Graph & Edge classes + Dijkstra & A* logic
├── sample_data.py   # Predefined city map data and coordinates
├── main.py          # Interactive CLI and demo mode (visualization optional)
├── requirements.txt # Optional visualization dependencies
└── README.md        # Project documentation (this file)
```

---

## ⚙️ How to Run

### ▶️ Install optional visualization dependencies (optional)
```bash
pip install -r requirements.txt
```

### ▶️ Run interactively
```bash
python main.py
```

### 🧪 Quick demo (sample data + auto-visualize if dependencies installed)
```bash
python main.py --demo
```

### 📄 Load your own CSV
You can also define your own graph connections:
```csv
u,v,distance,traffic_factor
A,B,4,1.0
A,C,2,1.2
B,D,5,1.1
C,E,10,1.3
D,E,2,1.0
E,Z,3,1.0
```
Save as `roads.csv`, then run the program and select **"Load from CSV"**.

---

## 🧮 Example Output
```
=== Smart Traffic Flow Optimizer ===
Algorithm: Dijkstra
Path: A -> B -> D -> E -> Z
Total effective distance: 14.00
```

---

## 🧰 Tech Stack
| Category | Technologies Used |
|-----------|-------------------|
| **Language** | Python 3 |
| **Concepts** | OOP, DSA, Graphs, Priority Queues, Heuristics |
| **Algorithms** | Dijkstra’s Algorithm, A* Search |
| **Visualization (optional)** | networkx, matplotlib |
| **Interface** | Command-line (CLI) |

---

## 🎯 Learning Outcomes
✔️ Designed a modular, object-oriented system using Python  
✔️ Applied **graph algorithms** (Dijkstra & A*) for real-world optimization  
✔️ Practiced DSA concepts: Graphs, Heaps, Priority Queues  
✔️ Implemented error handling, file I/O, and user interaction logic  
✔️ (Optional) Visualized graph and path using `networkx` + `matplotlib`

---


