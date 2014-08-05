graphene
========

A python package for processing graphs, currently supports loading adjacency matrix from csv, shortest paths calculation using Floyd-Warshall and/or a parallelized implementation of Dijkstra's algorithm.

Examples of usage are provided below.

The file graph.py contains the Graph object.

To instantiate a Graph object and add details about nodes:

```python
G = Graph()

G.add_node(node_id=1, node_label="a")
G.add_node(node_id="2", node_label="b")
G.add_node(3, "c")
G.add_node(4, "d")
G.add_node(5, "e")
```

To add edges to the graph with edge weights ( a default weight of 1.0 is assumed if edge weight is not provided)

```python
G.add_edge(source_id=1, target_id="2", edge_strength=0.1)
G.add_edge(2, 4, 0.3)
G.add_edge(4, 5)
```

To load a graph from an adjacency matrix provided as a csv (excel style csv), where the first row contains the target node ids and the first column of subsequent rows contains the source node id and the [row, column] cell contains edge weight as a float. If nothing is specified, the edge is assumed absent

```python
G.load_adjacency_matrix_from_csv("path_to_file.csv")
```

The classes Dijkstra and FloydWarshall are extended from Graph as the base class, so the same syntax for graph loading as shown above can be used.

```python
D = Dijkstra(num_threads)
```
If the num_threads parameter is not specified, it defaults to zero, essentially making the application a single threaded one. I would recommend using as many threads as there are processor cores.

After loading the graph (using any of the techniques shown above), it is necessary to start the shortest paths calculations as shown below:

```python
D.calculate_all_shortest_paths()
```
Now to obtain the shortest route from source node to target node:

```python
print D.get_shortest_route(source_id, target_id)
```
This will return a list of the ids of all the nodes encountered on moving from source node to target node.

To obtain the shortest path length:

```python
print D.get_shortest_path_length(source_id, target_id)
```
