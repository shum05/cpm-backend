from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import networkx as nx
import os
from task_scheduler import TaskScheduler
from critical_path import CriticalPath

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    scheduler = TaskScheduler(file_path)
    task_graph = scheduler.get_task_graph()
    
    cpm = CriticalPath(task_graph)
    critical_path, duration = cpm.compute_critical_path()

    return jsonify({'critical_path': critical_path, 'duration': duration})

if __name__ == '__main__':
    app.run(debug=True)
