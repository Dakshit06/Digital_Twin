"""
Configuration settings for CNC Digital Twin
Easy-to-modify central configuration
"""

# Data Generation Settings
DATA_ROWS = 2500
NUM_MACHINES = 2
NUM_OPERATIONS = 8
DATA_SEED = 42

# File Paths
DATASET_CSV = "data/digital_twin_cnc_operation.csv"
TELEMETRY_CSV = "data/telemetry.csv"
REPORT_OUTPUT_DIR = "reports/output"
MODELS_DIR = "analytics/models"

# Dashboard Settings
DASHBOARD_HOST = "127.0.0.1"
DASHBOARD_PORT = 5000
DASHBOARD_DEBUG = True
REFRESH_INTERVAL_SECONDS = 2

# ML Model Settings
TEST_SIZE = 0.25
RANDOM_STATE = 42
N_ESTIMATORS_REGRESSION = 120
N_ESTIMATORS_CLASSIFICATION = 150

# Alert Thresholds
VIBRATION_THRESHOLD_G = 1.2
CUTTING_FORCE_THRESHOLD_N = 600
SPINDLE_TEMP_CRITICAL_C = 80
SPINDLE_TEMP_WARNING_C = 70
SURFACE_ROUGHNESS_TOLERANCE_UM = 0.8
RUL_WARNING_MINUTES = 15

# Pipeline Simulation
DEFAULT_SIMULATION_ITERATIONS = 300
DEFAULT_SIMULATION_DELAY = 0.03
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_PATTERN = "cnc/+/telemetry"

# Report Settings
REPORT_TITLE = "CNC Machine Digital Twin Analysis Report"
REPORT_AUTHOR = "Digital Twin System"
FIGURE_DPI = 100
FIGURE_SIZE_WIDE = (10, 4)
FIGURE_SIZE_STANDARD = (8, 3)
