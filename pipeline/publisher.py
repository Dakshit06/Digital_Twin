"""
Publisher - Simulates CNC machine telemetry
Simplified version of edge/mqtt_publisher.py
"""
import random
import json
from datetime import datetime


def make_telemetry_payload(machine_id="CNC-01"):
    """Generate a single telemetry reading"""
    return {
        "ts": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "machine_id": machine_id,
        "spindle_rpm": random.randint(1000, 7000),
        "feed_rate": random.choice([500, 800, 1200]),
        "axis_x_pos": round(random.uniform(0, 200), 3),
        "axis_y_pos": round(random.uniform(0, 200), 3),
        "axis_z_pos": round(-random.uniform(0, 20), 3),
        "spindle_power": round(random.uniform(100, 800), 1),
        "vibration": {
            "x": round(random.uniform(0.05, 1.0), 4),
            "y": round(random.uniform(0.05, 1.0), 4),
            "z": round(random.uniform(0.05, 1.0), 4),
        },
    }


if __name__ == "__main__":
    # Demo: print sample payload
    sample = make_telemetry_payload()
    print("Sample CNC Telemetry:")
    print(json.dumps(sample, indent=2))
