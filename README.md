The objective of this project is to implement a visual representation of famous graph search algorithms.

To run the project:
- Create and activate a virtual environment
- pip install -r requirements.txt
- streamlit run app.py

Python implementation of the following graph search algorithms:

- BFS (Breadth First Search)
- DFS (Depth First Search)
- Dijkstra
- A*
- Greedy Best-First Search
- Bidirectional Search

How to use it:

- Pick the number of nodes, or generate a new random graph
- Pick a starting node and a goal node (by default the leftmost and rightmost nodes)
- Choose between a weighted graph (each edge costs its length) and an unweighted one (every edge costs 1), and see which algorithms change their answer
- "Begin search" animates the selected algorithm step by step, then highlights the path it found
- "Race all six" runs every algorithm on the same graph and compares the nodes explored, the hops and the total cost of each path

Project structure:

- `app.py`: the Streamlit interface
- `graph.py`: the `Graph` class (neighbours, edge costs, A* heuristic)
- `search_algorithms.py`: the six search algorithms
- `utils.py`: graph generation, plotting and animation
