/**
 * The KnightTourMCTS class implements a solution to the Knight's Tour problem using a Monte Carlo Tree Search (MCTS)
 * framework with CNN guidance. The CNN is represented here as a dummy evaluator that returns a value based on the
 * current progress (i.e. depth / (n*n)). The program reads the board size and time constraint from the user,
 * and then attempts to find a complete tour using MCTS. If a solution is found, the knight's path, board configuration,
 * and move log are saved into three text files: path.txt, board.txt, and moves.txt.
 *
 * MCTS Phases:
 * - Selection: Traverse the tree using the UCT formula.
 * - Expansion: Expand the current node by generating all legal knight moves.
 * - Simulation/Evaluation: Instead of full random rollout, we use a CNN evaluator (stub) to estimate the value.
 * - Backpropagation: Update the node statistics along the path.
 *
 * Usage:
 * 1. Run the program.
 * 2. Enter the board size (n).
 * 3. Enter the time constraint in minutes.
 * 4. The program will attempt to find a solution within the given time.
 * 5. If a solution is found, the knight's path, board configuration, and move log are saved in path.txt, board.txt, and moves.txt.
 */
import java.io.*;
import java.util.*;

public class KnightTourMCTS {

    public static void main(String[] args) throws IOException {
        try (Scanner sc = new Scanner(System.in)) {

            System.out.println("+++========================== Knight's Tour Problem (MCTS + CNN) ==========================+++");
            System.out.println("+++===========================================================================================+++");
            System.out.print("Enter board size (n): ");
            int n = sc.nextInt();
            System.out.println("+++===========================================================================================+++");

            System.out.println("+++========================== Time Constraint Limit =========================================+++");
            System.out.print("Enter time constraint in minutes: ");
            int timeLimitInMinutes = sc.nextInt();
            System.out.println("+++===========================================================================================+++");
            
            long timeConstraint = timeLimitInMinutes * 60L * 1000L;

            Problem problem = new Problem(n);
            Node root = new Node(0, 0, 1, null);
            MCTS mcts = new MCTS();
            Node result = mcts.search(problem, root, timeConstraint);

            if (result != null) {
                System.out.println("A solution was found.");
                printPath(result, n);
                printBoard(result, n);
            } else {
                System.out.println("No solution exists within the time constraint.");
            }
        } catch (OutOfMemoryError e) {
            try (BufferedWriter logWriter = new BufferedWriter(new FileWriter("OutOfMem.txt"))) {
                Runtime runtime = Runtime.getRuntime();
                System.out.println("Out of Memory Error occurred.");
                logWriter.write("Out of Memory Error occurred.\n");
                System.out.println("Maximum memory: " + (runtime.maxMemory() / 1024 / 1024) + " MB");
                logWriter.write("Maximum memory: " + (runtime.maxMemory() / 1024 / 1024) + " MB\n");
                System.out.println("Total memory: " + (runtime.totalMemory() / 1024 / 1024) + " MB");
                logWriter.write("Total memory: " + (runtime.totalMemory() / 1024 / 1024) + " MB\n");
                System.out.println("Free memory: " + (runtime.freeMemory() / 1024 / 1024) + " MB");
                logWriter.write("Free memory: " + (runtime.freeMemory() / 1024 / 1024) + " MB\n");
                System.out.println("Used memory: " + ((runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024) + " MB");
                logWriter.write("Used memory: " + ((runtime.totalMemory() - runtime.freeMemory()) / 1024 / 1024) + " MB\n");
                System.err.println("Error: Ran out of memory. Please try a smaller board size.");
                logWriter.write("Error: Ran out of memory. Please try a smaller board size.\n");
            } catch (IOException ex) {
                System.err.println("An unexpected error occurred: " + ex.getMessage());
            }
        } catch (IllegalArgumentException e) {
            System.err.println("An unexpected error occurred: " + e.getMessage());
        }
    }

    // Node class for MCTS. Each node represents a board state.
    static class Node {
        int x, y, depth;
        Node parent;
        List<Node> children;
        int visitCount;
        double totalValue;  // cumulative value from simulations

        public Node(int x, int y, int depth, Node parent) {
            this.x = x;
            this.y = y;
            this.depth = depth;
            this.parent = parent;
            this.children = new ArrayList<>();
            this.visitCount = 0;
            this.totalValue = 0.0;
        }

        // Check if the node is a terminal (goal) state.
        boolean isTerminal(Problem problem) {
            return depth == problem.n * problem.n;
        }

        // Check if node is fully expanded (all valid moves are generated)
        boolean isFullyExpanded(Problem problem) {
            List<int[]> moves = Arrays.asList(problem.moves);
            int validMoves = 0;
            for (int[] move : moves) {
                int newX = x + move[0];
                int newY = y + move[1];
                if (problem.isValid(this, newX, newY)) {
                    validMoves++;
                }
            }
            return children.size() == validMoves;
        }
    }

    // Problem class representing the Knight's Tour problem.
    static class Problem {
        int n;
        // possible moves for the knight
        int[][] moves = { { -2, -1 }, { -1, -2 }, { 1, -2 }, { 2, -1 },
                          { 2, 1 }, { 1, 2 }, { -1, 2 }, { -2, 1 } };

        public Problem(int n) {
            this.n = n;
        }
        
        // Check if the node state is a complete tour
        boolean isGoal(Node node) {
            return node.depth == n * n;
        }
        
        // Generate valid child nodes for a given node.
        List<Node> expand(Node node) {
            List<Node> children = new ArrayList<>();
            for (int[] move : moves) {
                int newX = node.x + move[0];
                int newY = node.y + move[1];
                if (isValid(node, newX, newY)) {
                    Node child = new Node(newX, newY, node.depth + 1, node);
                    children.add(child);
                }
            }
            return children;
        }
        
        // Check if a move to (x, y) is within bounds and not already visited.
        boolean isValid(Node node, int x, int y) {
            if (x < 0 || y < 0 || x >= n || y >= n) {
                return false;
            }
            Node current = node;
            while (current != null) {
                if (current.x == x && current.y == y) {
                    return false;
                }
                current = current.parent;
            }
            return true;
        }
    }

    // Dummy CNN evaluator (stub) that returns a heuristic value for a node.
    // For example, a simple evaluation can be the ratio of visited cells.
    static class CNN {
        static double evaluate(Node node, Problem problem) {
            // Higher depth means more progress, so value is proportional to depth.
            // In a real CNN, you would input the board state and get a value prediction.
            return (double) node.depth / (problem.n * problem.n);
        }
    }

    // MCTS class implements the Monte Carlo Tree Search algorithm.
    static class MCTS {
        
        private final double explorationConstant = Math.sqrt(2);

        // The search method now logs moves into "moves.txt".
        public Node search(Problem problem, Node root, long timeConstraint) throws IOException {
            
            long startTime = System.currentTimeMillis();
            int iterations = 0;
            try (BufferedWriter movesWriter = new BufferedWriter(new FileWriter("moves.txt"))) {
                while (System.currentTimeMillis() - startTime < timeConstraint) {
                    Node selected = select(root, problem);
                    if (selected == null) {
                        break; // no further expansion possible
                    }
                    movesWriter.write("Iteration " + iterations + ": Selected Node (" 
                            + selected.x + "," + selected.y + ") Depth " + selected.depth + "\n");
                    
                    double reward;
                    if (!selected.isTerminal(problem)) {
                        // Expand the node if not terminal
                        List<Node> children = problem.expand(selected);
                        for (Node child : children) {
                            if (!selected.children.contains(child)) {
                                selected.children.add(child);
                                movesWriter.write("    Expanded to (" + child.x + "," + child.y 
                                        + ") Depth " + child.depth + "\n");
                            }
                        }
                        // Choose one child randomly for simulation
                        if (!selected.children.isEmpty()) {
                            selected = selected.children.get(new Random().nextInt(selected.children.size()));
                        }
                    }
                    // Use CNN evaluation as simulation result
                    reward = CNN.evaluate(selected, problem);
                    // If it's a goal state, assign maximum reward
                    if (problem.isGoal(selected)) {
                        reward = 1.0;
                    }
                    backpropagate(selected, reward);
                    
                    // Log simulation result and backpropagation
                    movesWriter.write("    Simulation reward: " + reward + "\n");
                    
                    // If a terminal state (complete tour) is found, return it
                    if (problem.isGoal(selected)) {
                        movesWriter.write("Goal reached at iteration " + iterations + "\n");
                        movesWriter.flush();
                        long elapsedTime = System.currentTimeMillis() - startTime;
    System.out.printf("Time spent: %.3f seconds\n", elapsedTime/1000.0);
    System.out.println("Iterations: " + iterations);
    return selected;
                    }
                    iterations++;
                }
                movesWriter.write("Search ended at iteration " + iterations + "\n");
                movesWriter.flush();
            }
            long elapsedTime = System.currentTimeMillis() - startTime;
System.out.printf("Time spent: %.3f seconds\n", elapsedTime/1000.0); 
            System.out.println("Iterations: " + iterations);
            return null;
        }

        // Selection phase: traverse the tree using the UCT formula.
        private Node select(Node node, Problem problem) {
            while (!node.children.isEmpty()) {
                if (!node.isFullyExpanded(problem)) {
                    return node;
                }
                Node bestChild = null;
                double bestUCT = -Double.MAX_VALUE;
                for (Node child : node.children) {
                    double uctValue;
                    if (child.visitCount == 0) {
                        uctValue = Double.MAX_VALUE;
                    } else {
                        double exploitation = child.totalValue / child.visitCount;
                        double exploration = explorationConstant * Math.sqrt(Math.log(node.visitCount + 1) / child.visitCount);
                        uctValue = exploitation + exploration;
                    }
                    if (uctValue > bestUCT) {
                        bestUCT = uctValue;
                        bestChild = child;
                    }
                }
                if (bestChild == null) {
                    break;
                }
                node = bestChild;
                if (problem.isGoal(node)) {
                    break;
                }
            }
            return node;
        }

        // Backpropagation: update statistics along the path.
        private void backpropagate(Node node, double reward) {
            while (node != null) {
                node.visitCount++;
                node.totalValue += reward;
                node = node.parent;
            }
        }
    }

    // Print board configuration using the node's parent chain (path).
    static void printBoard(Node node, int n) throws IOException {
        int[][] board = new int[n][n];
        Node current = node;
        while (current != null) {
            board[current.x][current.y] = current.depth;
            current = current.parent;
        }
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("board.txt"))) {
            for (int i = n - 1; i >= 0; i--) {
                for (int j = 0; j < n; j++) {
                    writer.write(String.format("%4d ", board[i][j]));
                }
                writer.write("\n");
            }
        }
    }

    static void printPath(Node node, int n) throws IOException {
        List<Node> path = new ArrayList<>();
        Node current = node;
        while (current != null) {
            path.add(current);
            current = current.parent;
        }
        Collections.reverse(path);
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("path.txt"))) {
            writer.write("Knight Tour Path:\n");
            for (Node step : path) {
                char col = (char) ('a' + step.y);
                int row = step.x + 1;
                writer.write(String.format("Step %d: (%d, %d) -> %c%d%n", step.depth, step.x, step.y, col, row));
            }
        }
    }
}
