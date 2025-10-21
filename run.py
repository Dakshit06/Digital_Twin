"""
Main Entry Point - Run the complete CNC Digital Twin system
Orchestrates data generation, analysis, and dashboard
"""
import os
import sys
import argparse

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from data.generate_dataset import synthesize
from config.settings import DATASET_CSV, DATA_ROWS, NUM_MACHINES, NUM_OPERATIONS, DATA_SEED
import pandas as pd


def print_banner():
    """Print welcome banner"""
    print("\n" + "="*70)
    print("  🏭 CNC MACHINE DIGITAL TWIN SYSTEM")
    print("  Real-time Monitoring | Predictive Analytics | Visualization")
    print("="*70 + "\n")


def generate_data():
    """Generate synthetic dataset"""
    print("📊 Step 1: Generating synthetic dataset...")
    print(f"   Rows: {DATA_ROWS}")
    print(f"   Machines: {NUM_MACHINES}")
    print(f"   Operations: {NUM_OPERATIONS}")
    
    df = synthesize(rows=DATA_ROWS, machines=NUM_MACHINES, operations=NUM_OPERATIONS, seed=DATA_SEED)
    
    csv_path = os.path.join(os.path.dirname(__file__), DATASET_CSV)
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df.to_csv(csv_path, index=False)
    
    print(f"   ✓ Dataset saved: {csv_path}")
    print(f"   ✓ {len(df)} records generated\n")


def run_analytics():
    """Run ML analysis"""
    print("🤖 Step 2: Running machine learning analysis...")
    
    from analytics.analyze import run_full_analysis
    models, metrics, insights = run_full_analysis()
    
    print()


def generate_report():
    """Generate PDF report"""
    print("📄 Step 3: Generating comprehensive report...")
    
    from reports.analyze_and_report import main as generate_pdf_report
    generate_pdf_report()
    
    print()


def launch_dashboard():
    """Launch web dashboard"""
    print("🌐 Step 4: Launching interactive dashboard...")
    print()
    
    from dashboard.app import run_dashboard
    run_dashboard()


def main():
    """Main orchestrator"""
    parser = argparse.ArgumentParser(
        description='CNC Digital Twin - Complete System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run everything (recommended)
  python run.py
  
  # Run only data generation
  python run.py --data-only
  
  # Run only analysis
  python run.py --analysis-only
  
  # Run only dashboard
  python run.py --dashboard-only
  
  # Skip dashboard (run data + analysis only)
  python run.py --no-dashboard
        """
    )
    
    parser.add_argument('--data-only', action='store_true', help='Only generate dataset')
    parser.add_argument('--analysis-only', action='store_true', help='Only run analysis (requires existing dataset)')
    parser.add_argument('--dashboard-only', action='store_true', help='Only launch dashboard (requires existing dataset)')
    parser.add_argument('--no-dashboard', action='store_true', help='Skip dashboard launch')
    
    args = parser.parse_args()
    
    print_banner()
    
    try:
        if args.data_only:
            generate_data()
        elif args.analysis_only:
            run_analytics()
            generate_report()
        elif args.dashboard_only:
            launch_dashboard()
        else:
            # Full pipeline
            generate_data()
            run_analytics()
            generate_report()
            
            if not args.no_dashboard:
                launch_dashboard()
            else:
                print("✅ All steps complete!")
                print("\nTo launch dashboard later, run:")
                print("   python dashboard/app.py")
                print()
    
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
