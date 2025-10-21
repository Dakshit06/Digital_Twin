"""
Collector - Collects telemetry and saves to CSV
Simplified version of ingest/mqtt_to_influx.py with CSV fallback
"""
import os
import csv
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import TELEMETRY_CSV


def save_telemetry_to_csv(payload):
    """Save a telemetry payload to CSV file"""
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', TELEMETRY_CSV))
    
    # Flatten the nested structure
    row = {
        'timestamp': payload.get('ts'),
        'machine_id': payload.get('machine_id'),
        'spindle_rpm': payload.get('spindle_rpm'),
        'feed_rate': payload.get('feed_rate'),
        'axis_x_pos': payload.get('axis_x_pos'),
        'axis_y_pos': payload.get('axis_y_pos'),
        'axis_z_pos': payload.get('axis_z_pos'),
        'spindle_power': payload.get('spindle_power'),
        'vib_x': payload.get('vibration', {}).get('x'),
        'vib_y': payload.get('vibration', {}).get('y'),
        'vib_z': payload.get('vibration', {}).get('z'),
    }
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Write to CSV
    file_exists = os.path.exists(csv_path)
    with open(csv_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    
    print(f"✓ Saved telemetry: RPM={row['spindle_rpm']}, Power={row['spindle_power']}W")
    return csv_path


if __name__ == "__main__":
    from publisher import make_telemetry_payload
    
    # Demo: collect 5 samples
    print("Collecting 5 sample telemetry readings...\n")
    for i in range(5):
        payload = make_telemetry_payload()
        path = save_telemetry_to_csv(payload)
    
    print(f"\n✓ Data saved to: {path}")
