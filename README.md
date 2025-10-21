# 🏭 CNC Machine Digital Twin

**Production-Ready Digital Twin with Real-Time 3D Simulation & Predictive Analytics**

A complete digital twin system featuring:
- 🎮 **Interactive 3D Machine Simulation** (NEW!)
- 📊 **Real-time Monitoring Dashboard**
- 🤖 **Machine Learning Predictions**
- 📄 **Automated PDF Reports**

---

## ✨ NEW: 3D Simulation Feature!

**Experience your CNC machine in real-time 3D!**

- ✅ Fully interactive 3D model with realistic movements
- ✅ Live position tracking (X, Y, Z axes)
- ✅ Real-time spindle rotation based on RPM
- ✅ Mouse controls: rotate, zoom, pan
- ✅ Updates automatically from actual data

**Access**: http://127.0.0.1:5000 (after running `python run.py`)

👉 **See [3D_SIMULATION_GUIDE.md](3D_SIMULATION_GUIDE.md) for full details**

---

## 📁 Simple File Structure

```
cnc-digital-twin-vscode/
│
├── 📊 data/                              # Data Management
│   ├── generate_dataset.py               # Generate synthetic CNC data
│   ├── digital_twin_cnc_operation.csv    # Main comprehensive dataset
│   └── telemetry.csv                     # Real-time telemetry data
│
├── 🔄 pipeline/                          # Data Pipeline (Real-time)
│   ├── publisher.py                      # Simulate CNC telemetry
│   ├── collector.py                      # Collect and store data
│   └── simulator.py                      # Run full pipeline simulation
│
├── 🤖 analytics/                         # Machine Learning & Analysis
│   ├── analyze.py                        # Train ML models
│   ├── predict.py                        # Real-time predictions
│   └── models/                           # Saved ML models
│
├── 🌐 dashboard/                         # Web Dashboard
│   ├── app.py                            # Flask web server
│   ├── templates/                        # HTML files
│   │   ├── dashboard_3d.html             # 3D Simulation Dashboard ⭐ NEW
│   │   └── dashboard.html                # Classic 2D Dashboard
│   └── static/                           # CSS/JS files
│       └── js/
│           └── cnc_simulation.js         # 3D Simulation Engine ⭐ NEW
│
├── 📄 reports/                           # PDF Reports & Visualizations
│   ├── analyze_and_report.py             # Generate comprehensive PDF
│   ├── report_from_csv.py                # Quick CSV reports
│   └── output/                           # Generated reports & figures
│
├── ⚙️ config/                            # Configuration
│   └── settings.py                       # All settings in one place
│
├── 🚀 run.py                             # MAIN ENTRY POINT - RUN THIS!
├── 📖 README_SIMPLE.md                   # This file
└── 📦 requirements.txt                   # Python dependencies
```

---

## 🚀 Quickstart (3 Steps)

### 1. Install Dependencies
```powershell
.\.venv\Scripts\pip install -r requirements.txt
```

### 2. Run Everything
```powershell
.\.venv\Scripts\python run.py
```

That's it! This will:
- ✅ Generate 2,500 synthetic CNC records
- ✅ Train machine learning models (roughness & wear prediction)
- ✅ Create comprehensive PDF report
- ✅ Launch interactive dashboard at http://localhost:5000

### 3. Open Dashboard
Open your browser to: **http://localhost:5000**

---

## 📊 What You Get

### 1. **Comprehensive Dataset** (`data/digital_twin_cnc_operation.csv`)
- 2,500+ records of CNC operations
- 20 columns including:
  - Process parameters (spindle speed, feed rate, positions)
  - Sensor readings (vibration, temperature, force, acoustics)
  - Quality metrics (surface roughness, chatter detection)
  - Predictive indicators (tool wear, remaining useful life)

### 2. **Real-time Telemetry** (`data/telemetry.csv`)
- Simulated real-time CNC data
- Updates continuously during simulation
- Used for live dashboard monitoring

### 3. **Machine Learning Models** (`analytics/models/`)
- Surface roughness predictor (R² > 0.9)
- Tool wear classifier (Accuracy > 90%)
- Saved for real-time predictions

### 4. **PDF Analysis Report** (`reports/output/`)
- Executive summary with key findings
- Machine health analytics
- Predictive maintenance recommendations
- Visual charts and graphs
- Performance optimization insights

### 5. **Interactive Dashboard** (http://localhost:5000)
- Real-time monitoring charts
- Key performance indicators (KPIs)
- Temperature alerts
- Vibration analysis with chatter detection
- Surface quality metrics
- Auto-refreshes every 5 seconds

---

## 📖 Detailed Usage

### Run Individual Components

#### Generate Dataset Only
```powershell
.\.venv\Scripts\python run.py --data-only
```

#### Run Analytics Only
```powershell
.\.venv\Scripts\python run.py --analysis-only
```

#### Launch Dashboard Only
```powershell
.\.venv\Scripts\python run.py --dashboard-only
```

#### Run Without Dashboard
```powershell
.\.venv\Scripts\python run.py --no-dashboard
```

### Direct Component Access

#### Generate Custom Dataset
```powershell
.\.venv\Scripts\python data\generate_dataset.py --rows 5000 --machines 3 --operations 10
```

#### Run Real-time Simulation
```powershell
# 60-second simulation
.\.venv\Scripts\python pipeline\simulator.py --duration 60

# 500 iterations
.\.venv\Scripts\python pipeline\simulator.py --iterations 500 --delay 0.1
```

#### Train ML Models
```powershell
.\.venv\Scripts\python analytics\analyze.py
```

#### Make Predictions
```powershell
.\.venv\Scripts\python analytics\predict.py
```

#### Generate Report
```powershell
.\.venv\Scripts\python reports\analyze_and_report.py
```

#### Start Dashboard
```powershell
.\.venv\Scripts\python dashboard\app.py
```

---

## 🎯 Dataset Schema

| Column | Description | Example |
|--------|-------------|---------|
| `timestamp` | Data collection time | 2025-10-14T07:24:28Z |
| `machine_id` | CNC machine identifier | CNC-01 |
| `operation_id` | Operation/job ID | OP-001 |
| `spindle_speed_rpm` | Spindle rotation speed | 5365 |
| `feed_rate_mm_min` | Tool feed rate | 540.0 |
| `x_axis_position` | X-axis position (mm) | 171.72 |
| `y_axis_position` | Y-axis position (mm) | 139.474 |
| `z_axis_position` | Z-axis position (mm) | -1.884 |
| `vibration_x_g` | X-axis vibration | 0.2784 |
| `vibration_y_g` | Y-axis vibration | 0.2773 |
| `vibration_z_g` | Z-axis vibration | 0.1317 |
| `spindle_temp_c` | Spindle temperature (°C) | 78.25 |
| `motor_temp_c` | Motor temperature (°C) | 33.19 |
| `cutting_force_n` | Cutting force (N) | 273.14 |
| `acoustic_emission_ae` | Acoustic sensor RMS | 6.977 |
| `power_consumption_kw` | Power usage (kW) | 5.7 |
| `tool_wear_state` | 0=new, 1=medium, 2=worn | 0 |
| `surface_roughness_ra_um` | Surface quality (µm) | 0.394 |
| `chatter_detected` | Chatter flag | False |
| `remaining_useful_life_min` | Tool RUL (minutes) | 49.85 |

---

## ⚙️ Configuration

Edit `config/settings.py` to customize:

```python
# Data Generation
DATA_ROWS = 2500              # Number of records to generate
NUM_MACHINES = 2              # Number of CNC machines
NUM_OPERATIONS = 8            # Number of operations

# Dashboard
DASHBOARD_PORT = 5000         # Web server port
REFRESH_INTERVAL_SECONDS = 2  # Dashboard refresh rate

# Alert Thresholds
VIBRATION_THRESHOLD_G = 1.2   # Chatter detection threshold
SPINDLE_TEMP_CRITICAL_C = 80  # Critical temperature
SURFACE_ROUGHNESS_TOLERANCE_UM = 0.8  # Quality tolerance

# ML Models
N_ESTIMATORS_REGRESSION = 120  # Random forest trees (roughness)
N_ESTIMATORS_CLASSIFICATION = 150  # Random forest trees (wear)
```

---

## 📈 Dashboard Features

The interactive web dashboard shows:

- **KPI Cards**: Total records, average RPM, max temp, power, chatter events, roughness, RUL
- **Spindle Speed Chart**: Real-time RPM monitoring
- **Temperature Chart**: Spindle temperature with critical threshold line
- **Vibration Chart**: Vibration magnitude with chatter threshold
- **Quality Chart**: Surface roughness distribution histogram

**Auto-refresh**: Dashboard updates automatically every 5 seconds

---

## 🎨 Visualizations

The system generates multiple visualizations:

1. **Time-series Charts**
   - Spindle speed over time
   - Temperature monitoring with thresholds
   - Vibration analysis

2. **Histograms**
   - Surface roughness distribution
   - Quality control metrics

3. **Scatter Plots**
   - Cutting force vs. chatter events

4. **PDF Reports**
   - Professional reports with matplotlib charts
   - Executive summary and recommendations

---

## 🔧 Troubleshooting

### Dashboard won't start
```powershell
# Check if port 5000 is in use
# Change port in config/settings.py: DASHBOARD_PORT = 5001
```

### No data in dashboard
```powershell
# Generate dataset first
.\.venv\Scripts\python run.py --data-only
```

### Import errors
```powershell
# Reinstall dependencies
.\.venv\Scripts\pip install -r requirements.txt --force-reinstall
```

### Models not found error
```powershell
# Train models first
.\.venv\Scripts\python analytics\analyze.py
```

---

## 📚 Python API Examples

### Generate Data Programmatically
```python
from data.generate_dataset import synthesize

# Generate 1000 records
df = synthesize(rows=1000, machines=2, operations=5, seed=42)
df.to_csv("my_data.csv", index=False)
```

### Make Predictions
```python
from analytics.predict import predict_from_telemetry

telemetry = {
    'spindle_speed_rpm': 5500,
    'feed_rate_mm_min': 1000,
    'vibration_x_g': 0.8,
    'vibration_y_g': 0.7,
    'vibration_z_g': 0.6,
    'spindle_temp_c': 75,
    'motor_temp_c': 60,
    'cutting_force_n': 500,
    'acoustic_emission_ae': 8.5,
    'power_consumption_kw': 6.2,
}

predictions = predict_from_telemetry(telemetry)
print(f"Surface Roughness: {predictions['surface_roughness_um']:.3f} µm")
print(f"Tool Wear: {predictions['tool_wear']['wear_state']}")
```

### Run Analysis
```python
from analytics.analyze import run_full_analysis

models, metrics, insights = run_full_analysis()
print(f"Roughness R²: {metrics['roughness_r2']:.3f}")
print(f"Wear Accuracy: {metrics['wear_accuracy']:.3f}")
```

---

## 🔄 Data Flow

```
Physical CNC Machine (Simulated)
         ↓
  [Publisher] - Generates telemetry
         ↓
  [Collector] - Saves to CSV
         ↓
  [Dataset] - digital_twin_cnc_operation.csv
         ↓
  [Analytics] - Train ML models
         ↓
  [Dashboard] - Real-time visualization
         ↓
  [Reports] - PDF analysis reports
```

---

## 📊 Output Files

After running `run.py`, you'll find:

```
data/
├── digital_twin_cnc_operation.csv    # Main dataset (2,500 rows)
└── telemetry.csv                     # Real-time data

analytics/
└── models/
    ├── roughness_model.pkl           # Surface roughness ML model
    └── wear_model.pkl                # Tool wear ML model

reports/
└── output/
    ├── digital_twin_analysis_report.pdf  # Comprehensive PDF report
    └── figures/
        ├── spindle_temp_timeseries.png
        ├── surface_roughness_hist.png
        └── cutting_force_chatter.png
```

---

## 🎓 Learn More

- **Dataset Generation**: See `data/generate_dataset.py` for synthetic data logic
- **ML Models**: Check `analytics/analyze.py` for RandomForest training
- **Dashboard**: Explore `dashboard/app.py` for Flask + Plotly integration
- **Configuration**: All settings in `config/settings.py`

---

## 💡 Tips

1. **Start Simple**: Run `python run.py` first to see everything working
2. **Explore Dashboard**: Open http://localhost:5000 and watch live updates
3. **Read Reports**: Check `reports/output/` for PDF analysis
4. **Customize**: Edit `config/settings.py` to adjust thresholds and parameters
5. **Extend**: Add your own analytics in `analytics/` or dashboard views

---

## 🚀 Next Steps

- **Add Real Sensors**: Replace `publisher.py` with actual CNC sensor integration
- **Cloud Deployment**: Deploy dashboard to Azure/AWS
- **Advanced ML**: Add LSTM models for time-series prediction
- **Alerts**: Implement email/SMS notifications for critical events
- **3D Visualization**: Add Three.js for 3D tool path visualization

---

## 📞 Support

For issues or questions:
1. Check `config/settings.py` for configuration options
2. Review this README for usage examples
3. Check terminal output for error messages

---

**Version**: 2.0  
**Created**: October 2025  
**Status**: ✅ Production Ready

**🎉 Enjoy your CNC Digital Twin!**
