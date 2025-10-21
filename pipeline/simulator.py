"""
Simulator - Run complete pipeline simulation
Generates real-time telemetry data
"""
import os
import sys
import time
import argparse

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from publisher import make_telemetry_payload
from collector import save_telemetry_to_csv
from config.settings import DEFAULT_SIMULATION_ITERATIONS, DEFAULT_SIMULATION_DELAY


def run_simulation(iterations=DEFAULT_SIMULATION_ITERATIONS, delay=DEFAULT_SIMULATION_DELAY):
    """Run the full pipeline simulation"""
    print(f"🚀 Starting CNC Digital Twin Simulation")
    print(f"   Iterations: {iterations}")
    print(f"   Delay: {delay}s between readings")
    print(f"   Duration: ~{iterations * delay:.1f}s\n")
    
    for i in range(iterations):
        payload = make_telemetry_payload()
        save_telemetry_to_csv(payload)
        time.sleep(delay)
        
        if (i + 1) % 50 == 0:
            print(f"   Progress: {i + 1}/{iterations} readings collected")
    
    print(f"\n✅ Simulation complete! {iterations} telemetry readings collected.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run CNC pipeline simulation')
    parser.add_argument('--iterations', type=int, default=DEFAULT_SIMULATION_ITERATIONS,
                        help='Number of telemetry readings to generate')
    parser.add_argument('--delay', type=float, default=DEFAULT_SIMULATION_DELAY,
                        help='Delay between readings in seconds')
    parser.add_argument('--duration', type=float, default=None,
                        help='Run for specified duration in seconds (overrides iterations)')
    
    args = parser.parse_args()
    
    if args.duration:
        iterations = int(args.duration / args.delay)
        print(f"Running for {args.duration}s duration ({iterations} iterations)")
    else:
        iterations = args.iterations
    
    run_simulation(iterations=iterations, delay=args.delay)
