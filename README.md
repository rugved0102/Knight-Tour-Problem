# ♞ Knight's Tour — MCTS + CNN Visualizer

This project provides a Java-based implementation of the **Knight’s Tour Problem** using **Monte Carlo Tree Search (MCTS)** enhanced with a **CNN-inspired heuristic**, along with a visually rich **Pygame visualization** in Python.

---

## 🚀 Features

- 🔍 **Monte Carlo Tree Search (MCTS)** with exploration-exploitation strategy
- 🧠 **CNN-inspired evaluation function** for intelligent move selection
- ⏳ **Time constraint** input to limit search duration
- 📊 **Detailed logging** of iterations, execution time, and board states
- ✨ **Pygame-based visualization** with:
  - Glowing knight
  - Magical particle effects
  - Step-by-step animated traversal
  - Dynamic board resizing
  - Axis labeling and fading path trails

---

## 🛠️ Tech Stack

- **Java** — MCTS logic, CNN-guided evaluation, search and logging
- **Python (Pygame)** — Visualization of the knight’s path on the board

---

## 📦 Usage

### Run MCTS Solver (Java)
```bash
javac KnightTourMCTS.java
java KnightTourMCTS
```

- Enter board size (n)

- Enter time constraint in minutes

### Run Visualization (Python)
python Numbers_Visualization.py

### Project Structure
```
KnightTour_MCTS_CNN/
│
├── KnightTourMCTS.java        # Java implementation of MCTS + CNN
├── Numbers_Visualization.py   # Pygame visualization script
└── README.md
```
### Acknowledgements
This project was developed as part of a coursework assignment at VIT Pune for the Design and Analysis of Algorithms course.
