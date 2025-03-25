from flask import Flask, jsonify, render_template
import random

app = Flask(__name__, template_folder="templates", static_folder="static")

# Define bus stops (stations)
bus_stops = [
    {"id": 1, "name": "Vile Parle", "lat": 19.1000, "lon": 72.8370},
    {"id": 2, "name": "Santacruz", "lat": 19.0800, "lon": 72.8550},
    {"id": 3, "name": "Andheri", "lat": 19.1197, "lon": 72.8466}
]

# Define bus routes with predefined paths
bus_routes = {
    1: [(19.1000, 72.8370), (19.0900, 72.8450), (19.0800, 72.8550)],  # Vile Parle -> Santacruz
    2: [(19.0800, 72.8550), (19.0990, 72.8600), (19.1197, 72.8466)],  # Santacruz -> Andheri
    3: [(19.1000, 72.8370), (19.1100, 72.8420), (19.1197, 72.8466)]   # Vile Parle -> Andheri
}

# Simulated buses
buses = [
    {"id": 1, "route": 1, "current_index": 0, "eta_minutes": random.randint(5, 15)},
    {"id": 2, "route": 2, "current_index": 0, "eta_minutes": random.randint(5, 15)},
    {"id": 3, "route": 3, "current_index": 0, "eta_minutes": random.randint(5, 15)}
]

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/mumbai-buses", methods=["GET"])
def get_bus_data():
    """Returns real-time bus locations and ETA for Mumbai buses."""
    for bus in buses:
        route = bus_routes[bus["route"]]
        bus["current_index"] = (bus["current_index"] + 1) % len(route)
        bus["lat"], bus["lon"] = route[bus["current_index"]]
        bus["eta_minutes"] = random.randint(5, 15)

    return jsonify({"buses": buses, "stops": bus_stops})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
