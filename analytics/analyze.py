"""
Analytics - Train ML models and perform analysis
Comprehensive machine learning for predictive maintenance
"""
import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, mean_absolute_error

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import (
    DATASET_CSV, MODELS_DIR, TEST_SIZE, RANDOM_STATE,
    N_ESTIMATORS_REGRESSION, N_ESTIMATORS_CLASSIFICATION
)


class CNCAnalytics:
    """Main analytics class for CNC digital twin"""
    
    def __init__(self, dataset_path=None):
        if dataset_path is None:
            dataset_path = os.path.join(os.path.dirname(__file__), '..', DATASET_CSV)
        self.dataset_path = dataset_path
        self.df = None
        self.models = {}
        self.metrics = {}
        
    def load_data(self):
        """Load dataset"""
        print(f"📊 Loading dataset from: {self.dataset_path}")
        self.df = pd.read_csv(self.dataset_path, parse_dates=['timestamp'])
        print(f"   ✓ Loaded {len(self.df)} records")
        return self.df
    
    def train_models(self):
        """Train all ML models"""
        print("\n🤖 Training machine learning models...")
        
        # Feature columns
        features = [
            'spindle_speed_rpm', 'feed_rate_mm_min', 
            'vibration_x_g', 'vibration_y_g', 'vibration_z_g',
            'spindle_temp_c', 'motor_temp_c', 
            'cutting_force_n', 'acoustic_emission_ae', 
            'power_consumption_kw'
        ]
        
        df_clean = self.df.dropna(subset=features + ['surface_roughness_ra_um', 'tool_wear_state'])
        
        # Train surface roughness predictor
        print("\n   Training surface roughness model...")
        X = df_clean[features].values
        y_roughness = df_clean['surface_roughness_ra_um'].values
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_roughness, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        
        model_roughness = RandomForestRegressor(
            n_estimators=N_ESTIMATORS_REGRESSION, 
            random_state=RANDOM_STATE, 
            n_jobs=-1
        )
        model_roughness.fit(X_train, y_train)
        
        y_pred = model_roughness.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        self.models['roughness'] = model_roughness
        self.metrics['roughness_r2'] = r2
        self.metrics['roughness_mae'] = mae
        print(f"   ✓ Roughness model: R²={r2:.3f}, MAE={mae:.3f} µm")
        
        # Train tool wear classifier
        print("\n   Training tool wear model...")
        y_wear = df_clean['tool_wear_state'].values.astype(int)
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_wear, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        
        model_wear = RandomForestClassifier(
            n_estimators=N_ESTIMATORS_CLASSIFICATION, 
            random_state=RANDOM_STATE, 
            n_jobs=-1
        )
        model_wear.fit(X_train, y_train)
        
        y_pred = model_wear.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        
        self.models['wear'] = model_wear
        self.metrics['wear_accuracy'] = acc
        print(f"   ✓ Wear model: Accuracy={acc:.3f}")
        
        return self.models, self.metrics
    
    def save_models(self):
        """Save trained models to disk"""
        models_path = os.path.join(os.path.dirname(__file__), MODELS_DIR)
        os.makedirs(models_path, exist_ok=True)
        
        print(f"\n💾 Saving models to: {models_path}")
        for name, model in self.models.items():
            path = os.path.join(models_path, f'{name}_model.pkl')
            joblib.dump(model, path)
            print(f"   ✓ Saved {name} model")
    
    def generate_insights(self):
        """Generate key insights from data"""
        print("\n📈 Generating insights...")
        
        insights = {
            'total_records': len(self.df),
            'machines': self.df['machine_id'].nunique(),
            'operations': self.df['operation_id'].nunique(),
            'avg_spindle_rpm': float(self.df['spindle_speed_rpm'].mean()),
            'avg_temp': float(self.df['spindle_temp_c'].mean()),
            'chatter_events': int(self.df['chatter_detected'].sum()),
            'chatter_rate': float(self.df['chatter_detected'].mean()),
            'avg_roughness': float(self.df['surface_roughness_ra_um'].mean()),
            'avg_rul': float(self.df['remaining_useful_life_min'].mean()),
        }
        
        for key, value in insights.items():
            print(f"   {key}: {value}")
        
        return insights


def run_full_analysis(dataset_path=None):
    """Run complete analysis pipeline"""
    print("="*60)
    print("CNC DIGITAL TWIN - ANALYTICS")
    print("="*60)
    
    analytics = CNCAnalytics(dataset_path)
    analytics.load_data()
    analytics.train_models()
    analytics.save_models()
    insights = analytics.generate_insights()
    
    print("\n✅ Analysis complete!")
    print("="*60)
    
    return analytics.models, analytics.metrics, insights


if __name__ == "__main__":
    run_full_analysis()
