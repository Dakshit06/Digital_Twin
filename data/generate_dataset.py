import os
import math
import random
from datetime import datetime, timedelta
import argparse
import pandas as pd
import numpy as np


def synthesize(rows=2000, machines=1, operations=5, seed=42, start_time=None):
    rng = np.random.default_rng(seed)
    if start_time is None:
        start_time = datetime.utcnow()

    # Prepare sequences
    timestamps = [start_time + timedelta(seconds=i) for i in range(rows)]
    machine_ids = [f"CNC-{i+1:02d}" for i in range(machines)]
    operation_ids = [f"OP-{i+1:03d}" for i in range(operations)]

    # Wear progression across the dataset (0..1)
    wear_progress = np.linspace(0, 1, rows)

    records = []
    op_idx = 0
    for i in range(rows):
        ts = timestamps[i]
        machine_id = machine_ids[i % machines]
        # Rotate operations with occasional repeats
        if i % max(1, rows // (operations * machines)) == 0 and i > 0:
            op_idx = (op_idx + 1) % operations
        operation_id = operation_ids[op_idx]

        # Core process parameters
        spindle_speed_rpm = int(rng.normal(5000, 1200))
        spindle_speed_rpm = int(np.clip(spindle_speed_rpm, 800, 12000))
        feed_rate_mm_min = float(np.clip(rng.normal(800, 250), 100, 2000))

        # Axis positions (bounded work envelope)
        x_axis_position = float(np.round(np.clip(rng.uniform(0, 200), 0, 200), 3))
        y_axis_position = float(np.round(np.clip(rng.uniform(0, 200), 0, 200), 3))
        z_axis_position = float(np.round(-np.clip(rng.uniform(0, 20), 0, 20), 3))

        # Wear state grows with wear_progress, add noise
        wear_score = wear_progress[i] + 0.1 * rng.random()
        if wear_score < 0.33:
            tool_wear_state = 0  # new
        elif wear_score < 0.66:
            tool_wear_state = 1  # medium
        else:
            tool_wear_state = 2  # worn

        # Cutting force correlates with feed and speed (simplified)
        cutting_force_n = float(np.clip(0.3 * feed_rate_mm_min + 0.02 * spindle_speed_rpm + rng.normal(0, 30), 50, 2000))

        # Vibration components increase with wear and force
        vib_base = 0.15 + 0.8 * wear_score + 0.0003 * cutting_force_n
        vib_x = float(np.round(np.clip(rng.normal(vib_base, 0.1), 0.05, 2.5), 4))
        vib_y = float(np.round(np.clip(rng.normal(vib_base * 0.9, 0.1), 0.05, 2.5), 4))
        vib_z = float(np.round(np.clip(rng.normal(vib_base * 0.7, 0.1), 0.05, 2.5), 4))

        # Acoustic emission correlates with force and wear
        acoustic_emission_ae = float(np.round(np.clip(0.02 * cutting_force_n + 2.0 * wear_score + rng.normal(0, 1.5), 0, 80), 3))

        # Power consumption (kW) increases with speed and force
        power_consumption_kw = float(np.round(np.clip(0.001 * spindle_speed_rpm + 0.0008 * cutting_force_n + rng.normal(0, 0.15), 0.5, 15), 3))

        # Temperatures rise with power and speed
        spindle_temp_c = float(np.round(np.clip(25 + 0.008 * spindle_speed_rpm + 1.8 * power_consumption_kw + rng.normal(0, 1.0), 25, 95), 2))
        motor_temp_c = float(np.round(np.clip(25 + 1.2 * power_consumption_kw + rng.normal(0, 1.2), 25, 100), 2))

        # Surface roughness increases with wear and vibration
        vib_mag = math.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
        surface_roughness_ra_um = float(np.round(np.clip(0.25 + 0.6 * wear_score + 0.15 * vib_mag + rng.normal(0, 0.05), 0.1, 3.0), 3))

        # Chatter when vib magnitude and cutting force are high
        chatter_detected = bool(vib_mag > 1.2 and cutting_force_n > 600)

        # Remaining useful life (min) decreases with wear, add noise
        remaining_useful_life_min = float(np.round(np.clip(60 * (1.0 - wear_score) + rng.normal(0, 5), 0, 60), 2))

        record = {
            "timestamp": ts.isoformat(timespec="seconds") + "Z",
            "machine_id": machine_id,
            "operation_id": operation_id,
            "spindle_speed_rpm": spindle_speed_rpm,
            "feed_rate_mm_min": feed_rate_mm_min,
            "x_axis_position": x_axis_position,
            "y_axis_position": y_axis_position,
            "z_axis_position": z_axis_position,
            "vibration_x_g": vib_x,
            "vibration_y_g": vib_y,
            "vibration_z_g": vib_z,
            "spindle_temp_c": spindle_temp_c,
            "motor_temp_c": motor_temp_c,
            "cutting_force_n": cutting_force_n,
            "acoustic_emission_ae": acoustic_emission_ae,
            "power_consumption_kw": power_consumption_kw,
            "tool_wear_state": tool_wear_state,
            "surface_roughness_ra_um": surface_roughness_ra_um,
            "chatter_detected": chatter_detected,
            "remaining_useful_life_min": remaining_useful_life_min,
        }
        records.append(record)

    df = pd.DataFrame.from_records(records)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=2000)
    ap.add_argument("--machines", type=int, default=1)
    ap.add_argument("--operations", type=int, default=5)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", type=str, default=None, help="Output CSV path. Defaults to repo root digital_twin_cnc_operation.csv")
    args = ap.parse_args()

    df = synthesize(rows=args.rows, machines=args.machines, operations=args.operations, seed=args.seed)
    out_path = args.out or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "digital_twin_cnc_operation.csv"))
    df.to_csv(out_path, index=False)
    print(f"Wrote {out_path} with {len(df)} rows")


if __name__ == "__main__":
    main()
