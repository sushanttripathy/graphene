graphene
========

A Python package for processing graphs, currently supports loading adjacency matrix from csv, shortest paths calculation using Floyd-Warshall and/or a parallelized implementation of Dijkstra's algorithm.

To install change the current working directory to package root, and simply run the following command from a shell prompt.

```bash
sudo python setup.py install
```

Examples of usage are provided below.

The file graph.py contains the Graph object.

To instantiate a Graph object and add details about nodes:

```python
from graphene.graph import Graph

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
from graphene.dijkstra import Dijkstra

D = Dijkstra(num_threads=8)
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

The Floyd-Warshall algorithm for finding the shortest paths between all node pairs within a graph is implemented through the FloydWarshall class which is also derived from the Graph base class.

```python
from graphene.floydwarshall import FloydWarshall

F = FloydWarshall() #instantiate the object
```

After loading the graph into the object using any of the graph loading techniques mentioned above we have to initiate the calculation of all shortest paths as follows:

```python
F.calculate_all_shortest_paths()
```

The shortest path length between source node and target node can be found as such:

```python
print F.get_shortest_path_length(source_id , target_id)
```
It is important to note that the Floyd-Warshall algorithm does not keep track of the shortest route (i.e. the nodes encountered on the shortest path) instead it concerns itself with only calculating the shortest path length. Further, it is an iterative algorithm with poor support for parallellization (hence no parallellization is implemented for it here). From my personal experience, the parallellized Dijkstra outperforms Floyd-Warshall when processing a 1000 node graph with around 500,000 edges.

Now Graphene also supports calculation of cluster cohesion indices, currently only the E-I index is supported.

```python
from graphene.clusterindices import ClusterIndices
ei_index = ClusterIndices.calculate_EI_index(graph=G, cluster_nodes=cluster_indices)
```
