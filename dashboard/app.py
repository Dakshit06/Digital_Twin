"""
Dashboard - Interactive web visualization for CNC Digital Twin
Real-time monitoring and analytics dashboard
"""
import os
import sys
import json
from flask import Flask, render_template, jsonify
import pandas as pd
import plotly
import plotly.graph_objs as go
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import (
    DASHBOARD_HOST, DASHBOARD_PORT, DASHBOARD_DEBUG,
    DATASET_CSV, TELEMETRY_CSV,
    VIBRATION_THRESHOLD_G, SPINDLE_TEMP_CRITICAL_C,
    SURFACE_ROUGHNESS_TOLERANCE_UM
)

app = Flask(__name__)


def load_latest_data(limit=100):
    """Load most recent telemetry data"""
    dataset_path = os.path.join(os.path.dirname(__file__), '..', DATASET_CSV)
    
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path, parse_dates=['timestamp'])
        df = df.sort_values('timestamp', ascending=False).head(limit)
        return df
    return None


def create_spindle_chart(df):
    """Create spindle speed time series chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['spindle_speed_rpm'],
        mode='lines',
        name='Spindle Speed',
        line=dict(color='#2ecc71', width=2)
    ))
    
    fig.update_layout(
        title='Spindle Speed Over Time',
        xaxis_title='Time',
        yaxis_title='RPM',
        template='plotly_white',
        height=300
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_temperature_chart(df):
    """Create temperature monitoring chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['spindle_temp_c'],
        mode='lines',
        name='Spindle Temperature',
        line=dict(color='#e74c3c', width=2)
    ))
    
    # Add critical threshold line
    fig.add_trace(go.Scatter(
        x=[df['timestamp'].min(), df['timestamp'].max()],
        y=[SPINDLE_TEMP_CRITICAL_C, SPINDLE_TEMP_CRITICAL_C],
        mode='lines',
        name='Critical Threshold',
        line=dict(color='red', dash='dash')
    ))
    
    fig.update_layout(
        title='Temperature Monitoring',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)',
        template='plotly_white',
        height=300
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_vibration_chart(df):
    """Create vibration analysis chart"""
    # Calculate magnitude
    vib_mag = (df['vibration_x_g']**2 + df['vibration_y_g']**2 + df['vibration_z_g']**2)**0.5
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=vib_mag,
        mode='lines',
        name='Vibration Magnitude',
        line=dict(color='#9b59b6', width=2),
        fill='tozeroy'
    ))
    
    fig.add_trace(go.Scatter(
        x=[df['timestamp'].min(), df['timestamp'].max()],
        y=[VIBRATION_THRESHOLD_G, VIBRATION_THRESHOLD_G],
        mode='lines',
        name='Chatter Threshold',
        line=dict(color='orange', dash='dash')
    ))
    
    fig.update_layout(
        title='Vibration Analysis',
        xaxis_title='Time',
        yaxis_title='Magnitude (g)',
        template='plotly_white',
        height=300
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def create_quality_chart(df):
    """Create surface quality distribution"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['surface_roughness_ra_um'],
        nbinsx=30,
        name='Surface Roughness',
        marker_color='#3498db'
    ))
    
    fig.add_vline(
        x=SURFACE_ROUGHNESS_TOLERANCE_UM,
        line_dash="dash",
        line_color="red",
        annotation_text="Tolerance Limit"
    )
    
    fig.update_layout(
        title='Surface Quality Distribution',
        xaxis_title='Roughness Ra (µm)',
        yaxis_title='Frequency',
        template='plotly_white',
        height=300
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def calculate_kpis(df):
    """Calculate key performance indicators"""
    return {
        'total_records': len(df),
        'avg_spindle_rpm': float(df['spindle_speed_rpm'].mean()),
        'max_temp': float(df['spindle_temp_c'].max()),
        'avg_power': float(df['power_consumption_kw'].mean()),
        'chatter_events': int(df['chatter_detected'].sum()),
        'avg_roughness': float(df['surface_roughness_ra_um'].mean()),
        'avg_rul': float(df['remaining_useful_life_min'].mean()),
        'machines': df['machine_id'].nunique()
    }


@app.route('/')
def index():
    """Main dashboard page with 3D simulation"""
    return render_template('dashboard_3d.html')


@app.route('/2d')
def index_2d():
    """Original 2D dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/data')
def get_data():
    """API endpoint for dashboard data"""
    try:
        df = load_latest_data(limit=200)
        
        if df is None or df.empty:
            return jsonify({'error': 'No data available. Generate dataset first.'}), 404
        
        # Convert dataframe to list of dicts for 3D simulation
        raw_data = df.head(50).to_dict('records')
        
        data = {
            'kpis': calculate_kpis(df),
            'charts': {
                'spindle': create_spindle_chart(df),
                'temperature': create_temperature_chart(df),
                'vibration': create_vibration_chart(df),
                'quality': create_quality_chart(df)
            },
            'raw_data': raw_data,  # Add raw data for 3D simulation
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Error processing data: {str(e)}'}), 500


@app.route('/api/status')
def status():
    """System status endpoint"""
    dataset_path = os.path.join(os.path.dirname(__file__), '..', DATASET_CSV)
    telemetry_path = os.path.join(os.path.dirname(__file__), '..', TELEMETRY_CSV)
    
    return jsonify({
        'status': 'operational',
        'dataset_available': os.path.exists(dataset_path),
        'telemetry_available': os.path.exists(telemetry_path),
        'timestamp': datetime.utcnow().isoformat()
    })


def run_dashboard():
    """Start the dashboard server"""
    print("="*60)
    print("CNC DIGITAL TWIN - DASHBOARD")
    print("="*60)
    print(f"\n🌐 Starting dashboard server...")
    print(f"   URL: http://{DASHBOARD_HOST}:{DASHBOARD_PORT}")
    print(f"\n   Press Ctrl+C to stop\n")
    print("="*60)
    
    app.run(
        host=DASHBOARD_HOST,
        port=DASHBOARD_PORT,
        debug=DASHBOARD_DEBUG
    )


if __name__ == '__main__':
    run_dashboard()
