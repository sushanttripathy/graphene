__author__ = 'Sushant'

from graph import Graph
import threading
from prioritydict import PriorityDict


class Dijkstra(Graph):
    def __init__(self, num_threads=0, use_priority_queue=1):
        super(Dijkstra, self).__init__()
        self.shortest_paths = {}
        self.shortest_paths_guide = {}
        self.num_threads = num_threads
        if num_threads:
            self.lock = threading.Lock()
        self.use_priority_queue = use_priority_queue
        return

    def get_node_with_minimum_distance(self, q, distance, indices):
        min_dist = float("inf")
        min_ind = None
        min_node_id = None
        for ind, x in enumerate(q):
            if distance[x] < min_dist:
                min_ind = ind
                min_node_id = x
                min_dist = distance[x]
        indices.append(min_ind)
        return min_node_id

    def calculate_shortest_paths_from(self, source_id):
        distance = {}
        previous = {}
        q = None
        if self.use_priority_queue:
            q = PriorityDict()
        else:
            q = []
        ind = []
        distance[source_id] = 0
        for x in self.nodes:
            if x is not source_id:
                distance[x] = float("inf")
                previous[x] = None
            if self.use_priority_queue:
                q[x] = distance[x]
            else:
                q.append(x)

        while len(q):
            u = None
            if self.use_priority_queue:
                u = q.pop_smallest()
            else:
                u = self.get_node_with_minimum_distance(q, distance, ind)
                index = ind.pop()
                if type(index) is int:
                    del q[index]
                else:
                    break

            if isinstance(self.edges[u], dict):
                for v in self.edges[u]:
                    if v in q:
                        alt = distance[u] + self.edges[u][v].strength
                        if alt < distance[v]:
                            distance[v] = alt
                            previous[v] = u
                            if self.use_priority_queue:
                                q[v] = distance[v]
        if not self.num_threads:
            self.shortest_paths[source_id] = distance
            self.shortest_paths_guide[source_id] = previous
        else:
            self.lock.acquire()
            self.shortest_paths[source_id] = distance
            self.shortest_paths_guide[source_id] = previous
            self.lock.release()
        return

    def calculate_all_shortest_paths(self):
        if not self.num_threads:
            for source_id in self.nodes:
                self.calculate_shortest_paths_from(source_id)
        else:
            th = []
            for source_id in self.nodes:
                t = threading.Thread(target=self.calculate_shortest_paths_from, args=[source_id])
                t.start()
                th.append(t)

                if len(th) >= self.num_threads:
                    while len(th):
                        _t = th.pop()
                        _t.join()
            if len(th):
                while len(th):
                    _t = th.pop()
                    _t.join()
        return

    def get_shortest_path_length(self, source_id, target_id):
        if source_id in self.shortest_paths and isinstance(self.shortest_paths[source_id], dict):
            if target_id in self.shortest_paths[source_id]:
                return self.shortest_paths[source_id][target_id]
        return None

    def get_shortest_route(self, source_id, target_id, append_target=1):
        if source_id in self.shortest_paths_guide and isinstance(self.shortest_paths_guide[source_id], dict):
            if target_id in self.shortest_paths_guide[source_id]:
                r = []
                if self.shortest_paths_guide[source_id][target_id] is not source_id:
                    r = r + self.get_shortest_route(source_id, self.shortest_paths_guide[source_id][target_id], 0)
                r.append(self.shortest_paths_guide[source_id][target_id])
                if append_target:
                    r.append(target_id)
                return r
        return []


"""
G = Dijkstra(10, 1)

G.add_edge(1, 2, 0.1)
G.add_edge(1, 3, 0.3)
G.add_edge(2, 3, 0.1)
G.add_edge(3, 4, 0.1)
G.add_edge(2, 4, 0.5)

print "Calculating all possible shortest paths"
G.calculate_all_shortest_paths()
print "Shortest paths calculation finished"

print G.get_shortest_path_length(1, 4)
print G.get_shortest_route(1, 4)
"""



