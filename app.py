from flask import Flask, request, jsonify
from flask_cors import CORS
import networkx as nx

app = Flask(__name__)
CORS(app)

class CriticalPath:
    def __init__(self, task_graph):
        self.graph = task_graph

    def compute_critical_path(self):
        longest_path = nx.dag_longest_path(self.graph, weight='duration')
        longest_duration = sum(self.graph.nodes[node]["duration"] for node in longest_path)
        return longest_path, longest_duration

@app.route('/calculate', methods=['POST'])
def calculate_critical_path():
    data = request.json
    tasks = data.get("tasks", [])

    if not tasks:
        return jsonify({"error": "No tasks provided"}), 400

    task_graph = nx.DiGraph()
    for task in tasks:
        task_graph.add_node(task["name"], duration=task["duration"])
        for dependency in task["dependencies"]:
            task_graph.add_edge(dependency, task["name"])

    cpm = CriticalPath(task_graph)
    critical_path, duration = cpm.compute_critical_path()

    return jsonify({'critical_path': critical_path, 'duration': duration})

if __name__ == '__main__':
    app.run(debug=True)
