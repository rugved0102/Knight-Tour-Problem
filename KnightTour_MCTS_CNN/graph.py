import matplotlib.pyplot as plt
import numpy as np

# Board sizes
board_sizes = [8, 16, 32, 52, 255]

# Time values in seconds
time_values = {
    "DFS": [2.444, 60, 60, 60, None],
    "DFS + h1": [0.015, 0.04, 0.183, 1.247, 799.319],
    "DFS + h2": [0.016, 0.033, 0.168, 1.406, None],
    "MCTS": [6.677, 60.013, 60.017, 60.043, None]
}

# Nodes or Iterations (set to None where not applicable)
iterations_values = {
    "DFS": [3242064, 504734528, 230149371, 89663492, None],
    "DFS + h1": [63, 255, 1023, 2703, 65024],
    "DFS + h2": [63, 255, 1023, 2703, None],
    "MCTS": [721360, 5019762, 6817799, 7027687, None]
}

# Colors and markers
styles = {
    "DFS": {"color": "#e41a1c", "marker": "o", "linestyle": "-"},
    "DFS + h1": {"color": "#377eb8", "marker": "s", "linestyle": "--"},
    "DFS + h2": {"color": "#4daf4a", "marker": "D", "linestyle": "-."},
    "MCTS": {"color": "#984ea3", "marker": "^", "linestyle": ":"},
}

# Graph 1: Time vs Board Size
plt.figure(figsize=(10, 6))
for label, times in time_values.items():
    b_sizes, t_vals = zip(*[(b, t) for b, t in zip(board_sizes, times) if t is not None])
    plt.plot(b_sizes, t_vals, label=label, **styles[label])

plt.title("Time Comparison of Knight's Tour Algorithms")
plt.xlabel("Board Size (n)")
plt.ylabel("Time Taken (seconds)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("knight_tour_time_comparison.png")
plt.show()

# Graph 2: Nodes Expanded / Iterations vs Board Size (log scale)
plt.figure(figsize=(10, 6))
for label, nodes in iterations_values.items():
    b_sizes, n_vals = zip(*[(b, n) for b, n in zip(board_sizes, nodes) if n is not None])
    plt.plot(b_sizes, n_vals, label=label, **styles[label])

plt.title("Nodes Expanded / Iterations vs Board Size (Log Scale)")
plt.xlabel("Board Size (n)")
plt.ylabel("Nodes Expanded / Iterations (log scale)")
plt.yscale("log")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.savefig("knight_tour_nodes_comparison.png")
plt.show()
