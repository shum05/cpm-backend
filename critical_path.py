import networkx as nx

class CriticalPath:
    def __init__(self, task_graph):
        self.graph = task_graph

    def compute_critical_path(self):
        longest_path = nx.dag_longest_path(self.graph, weight='duration')
        longest_duration = sum(self.graph.nodes[node]["duration"] for node in longest_path)
        return longest_path, longest_duration
