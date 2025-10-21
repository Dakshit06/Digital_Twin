"""
Predict - Real-time predictions using trained models
"""
import os
import sys
import joblib
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import MODELS_DIR


class CNCPredictor:
    """Real-time prediction engine"""
    
    def __init__(self):
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load trained models"""
        models_path = os.path.join(os.path.dirname(__file__), MODELS_DIR)
        
        try:
            self.models['roughness'] = joblib.load(os.path.join(models_path, 'roughness_model.pkl'))
            self.models['wear'] = joblib.load(os.path.join(models_path, 'wear_model.pkl'))
            print("✓ Models loaded successfully")
        except FileNotFoundError:
            print("⚠ Models not found. Run analytics/analyze.py first to train models.")
            self.models = {}
    
    def predict_roughness(self, features):
        """Predict surface roughness"""
        if 'roughness' not in self.models:
            return None
        
        X = np.array([features])
        prediction = self.models['roughness'].predict(X)[0]
        return float(prediction)
    
    def predict_wear(self, features):
        """Predict tool wear state (0=new, 1=medium, 2=worn)"""
        if 'wear' not in self.models:
            return None
        
        X = np.array([features])
        prediction = self.models['wear'].predict(X)[0]
        probabilities = self.models['wear'].predict_proba(X)[0]
        
        return {
            'wear_state': int(prediction),
            'confidence': float(probabilities[prediction])
        }


# Singleton instance
predictor = CNCPredictor()


def predict_from_telemetry(telemetry):
    """
    Make predictions from raw telemetry data
    
    Args:
        telemetry: dict with keys like spindle_rpm, feed_rate, etc.
    
    Returns:
        dict with predictions
    """
    # Extract features in correct order
    features = [
        telemetry.get('spindle_speed_rpm', 5000),
        telemetry.get('feed_rate_mm_min', 800),
        telemetry.get('vibration_x_g', 0.5),
        telemetry.get('vibration_y_g', 0.5),
        telemetry.get('vibration_z_g', 0.5),
        telemetry.get('spindle_temp_c', 60),
        telemetry.get('motor_temp_c', 50),
        telemetry.get('cutting_force_n', 400),
        telemetry.get('acoustic_emission_ae', 5),
        telemetry.get('power_consumption_kw', 5),
    ]
    
    roughness = predictor.predict_roughness(features)
    wear = predictor.predict_wear(features)
    
    return {
        'surface_roughness_um': roughness,
        'tool_wear': wear
    }


if __name__ == "__main__":
    # Demo prediction
    sample_data = {
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
    
    print("Sample prediction:")
    predictions = predict_from_telemetry(sample_data)
    print(f"  Surface Roughness: {predictions['surface_roughness_um']:.3f} µm")
    print(f"  Tool Wear State: {predictions['tool_wear']['wear_state']} "
          f"(confidence: {predictions['tool_wear']['confidence']:.2%})")
