__author__ = 'Sushant'

from autovivification import AutoVivification

from collections import namedtuple

NodeDescriptor = namedtuple("NodeDescriptor", "id label")
GraphEdge = namedtuple("GraphEdge", "source target strength")


class Graph(object):
    def __init__(self):
        self.nodes = {}
        self.edges = AutoVivification()
        return

    def add_node(self, node_id, node_label):
        node = NodeDescriptor(id=node_id, label=node_label)
        self.nodes[node_id] = node
        return

    def add_edge(self, source_id, target_id, edge_strength=1):
        if not source_id in self.nodes:
            source_node = NodeDescriptor(id=source_id, label="")
            self.nodes[source_id] = source_node
        if not target_id in self.nodes:
            target_node = NodeDescriptor(id=target_id, label="")
            self.nodes[target_id] = target_node
        edge = GraphEdge(source=source_id, target=target_id, strength=edge_strength)
        self.edges[source_id][target_id] = edge
        return

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    @classmethod
    def get_float_val(cls, string_value):
        f = None
        try:
            f = float(string_value)
        except Exception as e:
            f = None
        return f

    def load_adjacency_matrix_from_csv(self, file_name, delimiter=","):
        import csv
        with open(file_name, "rb") as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            row_number = 0
            columns = {}
            rows = {}
            for row in reader:
                #print row
                if row_number == 0:
                    values_count = 0
                    for x in row:
                        if values_count != 0:
                            columns[values_count] = x
                        values_count += 1
                else:
                    values_count = 0
                    for x in row:
                        if values_count == 0:
                            rows[row_number] = x
                        else:
                            edge_strength = Graph.get_float_val(x)
                            if type(edge_strength) is float:
                                self.add_edge(rows[row_number], columns[values_count], edge_strength)
                        values_count += 1
                row_number += 1
            csv_file.close()
        return

"""
G = Graph()

G.add_node(1, "a")
G.add_node(2, "b")
G.add_node(3, "c")
G.add_node(4, "d")
G.add_node(5, "e")

G.add_edge(1, 2)
G.add_edge(2, 4)
G.add_edge(4, 5)

print G.get_nodes()
print G.get_edges()

edges = G.get_edges()

print edges[1][2].strength
"""

