__author__ = 'Sushant'

from graph import Graph
from graph import AutoVivification


class FloydWarshall(Graph):
    def __init__(self):
        super(FloydWarshall, self).__init__()
        self.minimum_distances = AutoVivification()
        return

    def calculate_all_shortest_paths(self):
        for m in self.nodes:
            for n in self.nodes:
                if m is not n:
                    if m in self.edges and n in self.edges[m]:
                        self.minimum_distances[m][n] = self.edges[m][n].strength
                    else:
                        self.minimum_distances[m][n] = float("inf")
                else:
                    self.minimum_distances[m][n] = 0

        for k in self.nodes:
            for i in self.nodes:
                for j in self.nodes:
                    if self.minimum_distances[i][j] > self.minimum_distances[i][k] + self.minimum_distances[k][j]:
                        self.minimum_distances[i][j] = self.minimum_distances[i][k] + self.minimum_distances[k][j]
        return

    def get_shortest_path_length(self, source_id, target_id):
        if source_id in self.minimum_distances and target_id in self.minimum_distances[source_id]:
            return self.minimum_distances[source_id][target_id]
        else:
            return None


"""
G = FloydWarshall()

G.add_edge(1 , 2, 0.1)
G.add_edge(1 , 3, 0.3)
G.add_edge(2 , 3, 0.1)
G.add_edge(3 , 4, 0.1)
G.add_edge(2 , 4, 0.5)

print "Calculating all possible shortest paths"
G.calculate_all_shortest_paths()
print "Shortest paths calculation finished"

print G.get_shortest_path_length(1 , 4)

"""
