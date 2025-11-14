import pandas as pd
import numpy as np
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.ml_models import blood_analysis_model

def create_sample_data():
    """Create sample training data"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'hemoglobin': np.random.normal(14.5, 1.5, n_samples),
        'wbc_count': np.random.normal(7500, 2000, n_samples),
        'rbc_count': np.random.normal(4.8, 0.5, n_samples),
        'platelets': np.random.normal(250000, 50000, n_samples),
        'glucose': np.random.normal(95, 20, n_samples),
        'cholesterol': np.random.normal(180, 30, n_samples),
        'hdl_cholesterol': np.random.normal(50, 10, n_samples),
        'ldl_cholesterol': np.random.normal(110, 25, n_samples),
        'triglycerides': np.random.normal(150, 40, n_samples),
        'alt': np.random.normal(25, 10, n_samples),
        'ast': np.random.normal(22, 8, n_samples),
        'alp': np.random.normal(100, 30, n_samples),
        'bilirubin_total': np.random.normal(0.8, 0.3, n_samples),
        'bilirubin_direct': np.random.normal(0.2, 0.1, n_samples),
        'bilirubin_indirect': np.random.normal(0.6, 0.2, n_samples),
        'creatinine': np.random.normal(0.9, 0.2, n_samples),
        'bun': np.random.normal(15, 5, n_samples),
        'sodium_level': np.random.normal(140, 3, n_samples),
        'potassium_level': np.random.normal(4.0, 0.5, n_samples),
        'chloride_level': np.random.normal(102, 3, n_samples),
        'calcium_level': np.random.normal(9.5, 0.5, n_samples),
        'protein_total': np.random.normal(7.0, 0.5, n_samples),
        'albumin': np.random.normal(4.0, 0.4, n_samples),
        'globulin': np.random.normal(3.0, 0.4, n_samples),
        'ag_ratio': np.random.normal(1.3, 0.2, n_samples),
        'tsh': np.random.normal(2.5, 1.0, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target labels based on abnormalities
    conditions = []
    for idx, row in df.iterrows():
        if row['hemoglobin'] < 12:
            conditions.append('ANEMIA')
        elif row['glucose'] > 140:
            conditions.append('DIABETES')
        elif row['alt'] > 56 or row['ast'] > 40:
            conditions.append('LIVER_DISEASE')
        elif row['creatinine'] > 1.3:
            conditions.append('KIDNEY_DISEASE')
        elif row['tsh'] > 4.0:
            conditions.append('THYROID_DISORDER')
        else:
            conditions.append('NORMAL')
    
    df['condition'] = conditions
    return df

if __name__ == "__main__":
    print("🔄 Creating sample training data...")
    # Create sample data
    sample_data = create_sample_data()
    
    # Split features and target
    X = sample_data.drop('condition', axis=1)
    y = sample_data['condition']
    
    print("🔄 Training ML model...")
    # Train model
    results = blood_analysis_model.train(X, y)
    print("✅ Model training completed!")
    print(f"📊 Accuracy: {results['accuracy']:.4f}")
    print(f"🔧 Features used: {results['features_used']}")
    print(f"📈 Training samples: {results['training_samples']}")