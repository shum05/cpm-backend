import pandas as pd
import networkx as nx

class TaskScheduler:
    def __init__(self, file_path):
        self.df = pd.read_csv(file_path)
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        for _, row in self.df.iterrows():
            task = row["Task ID"]
            duration = row["Duration (days)"]
            dependencies = str(row["Dependencies"]).split(",") if pd.notna(row["Dependencies"]) else []
            self.graph.add_node(task, duration=duration)
            for dep in dependencies:
                if dep.strip():
                    self.graph.add_edge(dep.strip(), task)

    def get_task_graph(self):
        return self.graph
