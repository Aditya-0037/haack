import os
import json
import time
import random
import threading
from flask import Flask, jsonify
from flask_cors import CORS
from google.cloud import monitoring_v3

# Setup GCP Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"
GCP_PROJECT_ID = "bubbly-access-491008-k5"

app = Flask(__name__)
CORS(app)

# Global data store for the live session
live_servers = []

# Load initial mock data
try:
    with open('mock_cloud_data.json', 'r') as f:
        live_servers = json.load(f)
    print(f"Successfully loaded {len(live_servers)} servers from mock_cloud_data.json")
except Exception as e:
    print(f"Error loading mock data: {e}")
    live_servers = []

def simulate_live_traffic():
    """
    Background worker that simulates real-time metric fluctuations.
    In a production environment, this would poll the GCP Monitoring API.
    """
    global live_servers
    
    # Initialize GCP Monitoring Client
    try:
        client = monitoring_v3.MetricServiceClient()
        print("✅ GCP Monitoring Client initialized successfully.")
    except Exception as e:
        print(f"⚠️ GCP Initialization Warning: {e}. Falling back to full simulation mode.")
        client = None

    while True:
        try:
            for server in live_servers:
                # ZOMBIE RULE: If CPU is -1 (Decommissioned) or baseline 0% (Zombie Node), skip updates.
                # This ensures anomalies stay static until 'fixed' by the user.
                if server.get("cpu_usage_percent") == -1 or (server.get("cpu_usage_percent") == 0 and server.get("network_traffic") == 0):
                    continue

                # --- HYBRID LOGIC ---
                # In a production environment, you would fetch real metrics here:
                # project_name = f"projects/{GCP_PROJECT_ID}"
                # results = client.list_time_series(
                #     request={
                #         "name": project_name,
                #         "filter": f'metric.type = "compute.googleapis.com/instance/cpu/utilization" AND resource.labels.instance_id = "{server["id"]}"',
                #         "interval": interval,
                #         "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                #     }
                # )
                
                # --- SIMULATION ENGINE ---
                # Fluctuate CPU usage by +/- 4% (Range: 1-100)
                cpu_delta = random.randint(-4, 4)
                new_cpu = server["cpu_usage_percent"] + cpu_delta
                server["cpu_usage_percent"] = max(1, min(100, new_cpu))

                # Fluctuate Network Traffic by +/- 15 MB/s (Minimum: 5 MB/s)
                net_delta = random.randint(-15, 15)
                new_net = server["network_traffic"] + net_delta
                server["network_traffic"] = max(5, new_net)

                # If the server has a GPU, fluctuate GPU usage too
                if server.get("gpu_count", 0) > 0 and server.get("max_gpu_usage_percent") is not None:
                    gpu_delta = random.randint(-2, 2)
                    new_gpu = server["max_gpu_usage_percent"] + gpu_delta
                    server["max_gpu_usage_percent"] = max(1, min(100, new_gpu))

            time.sleep(2)
        except Exception as e:
            print(f"Error in simulation loop: {e}")
            time.sleep(5)

# Initialize the background thread
if live_servers:
    sim_thread = threading.Thread(target=simulate_live_traffic, daemon=True)
    sim_thread.start()

@app.route('/api/servers', methods=['GET'])
def get_servers():
    """Returns the current state of all cloud servers."""
    return jsonify(live_servers)

if __name__ == '__main__':
    # Running on port 5000 for consumption by the Cloud Healer Frontend
    print("Cloud Healer Backend starting on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)
