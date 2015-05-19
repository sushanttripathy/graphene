__author__ = 'Sushant'

class ClusterIndices(object):
    @staticmethod
    def calculate_EI_index(graph, cluster_nodes, standardize=True):
        all_edges = graph.get_edges()
        external_connections_strength = 0.0
        internal_connections_strength = 0.0

        internal_nodes = len(cluster_nodes)
        external_nodes = len(graph.get_nodes()) - internal_nodes
        for node_id in cluster_nodes:
            if node_id in all_edges:
                for target_id in all_edges[node_id]:
                    if target_id in cluster_nodes:
                        #internal edge
                        internal_connections_strength += float(all_edges[node_id][target_id].strength)
                    else:
                        #external edge
                        external_connections_strength += float(all_edges[node_id][target_id].strength)

        if standardize:
            if internal_nodes and external_nodes:
                internal_connections_strength /= float(internal_nodes)
                external_connections_strength /= float(external_nodes)

        if (internal_connections_strength + external_connections_strength):
            return (external_connections_strength - internal_connections_strength)/(internal_connections_strength + external_connections_strength)
        else:
            return None