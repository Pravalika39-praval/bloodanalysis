import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import logging

logger = logging.getLogger(__name__)

class BloodAnalysisModel:
    """
    ML Model for comprehensive blood analysis prediction with 26 parameters
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'hemoglobin', 'wbc_count', 'rbc_count', 'platelets', 'glucose',
            'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'alt', 'ast', 'alp', 'bilirubin_total', 'bilirubin_direct', 
            'bilirubin_indirect', 'creatinine', 'bun', 'sodium_level', 
            'potassium_level', 'chloride_level', 'calcium_level', 'protein_total',
            'albumin', 'globulin', 'ag_ratio', 'tsh'
        ]
        self.model_path = model_path or 'ml_models/enhanced_blood_model.pkl'
        self.is_trained = False
        
        # Normal ranges for 26 blood parameters
        self.normal_ranges = {
            'hemoglobin': (12.0, 17.5),          # g/dL
            'wbc_count': (4000, 11000),          # cells/μL
            'rbc_count': (4.2, 6.1),             # million/μL
            'platelets': (150000, 450000),       # platelets/μL
            'glucose': (70, 140),                # mg/dL (fasting)
            'cholesterol': (0, 200),             # mg/dL
            'hdl_cholesterol': (40, 60),         # mg/dL (good cholesterol)
            'ldl_cholesterol': (0, 100),         # mg/dL (bad cholesterol)
            'triglycerides': (0, 150),           # mg/dL
            'alt': (7, 56),                      # U/L
            'ast': (10, 40),                     # U/L
            'alp': (44, 147),                    # U/L (Alkaline Phosphatase)
            'bilirubin_total': (0.1, 1.2),       # mg/dL
            'bilirubin_direct': (0.0, 0.3),      # mg/dL
            'bilirubin_indirect': (0.1, 1.1),    # mg/dL
            'creatinine': (0.6, 1.3),            # mg/dL
            'bun': (7, 20),                      # mg/dL
            'sodium_level': (135, 145),          # mmol/L
            'potassium_level': (3.5, 5.1),       # mmol/L
            'chloride_level': (98, 107),         # mmol/L
            'calcium_level': (8.5, 10.5),        # mg/dL
            'protein_total': (6.0, 8.3),         # g/dL
            'albumin': (3.4, 5.4),               # g/dL
            'globulin': (2.0, 3.5),              # g/dL
            'ag_ratio': (1.0, 2.0),              # Albumin/Globulin ratio
            'tsh': (0.4, 4.0)                    # mIU/L (Thyroid Stimulating Hormone)
        }
        
        # Possible health conditions to predict
        self.conditions = [
            'NORMAL',
            'ANEMIA',
            'DIABETES',
            'LIVER_DISEASE',
            'KIDNEY_DISEASE',
            'THYROID_DISORDER',
            'INFECTION',
            'HYPERLIPIDEMIA',
            'DEHYDRATION',
            'ELECTROLYTE_IMBALANCE'
        ]
        
        # Load model if exists
        self.load_model()
    
    def load_model(self) -> bool:
        """Load trained model from file"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data['model']
                    self.scaler = model_data['scaler']
                    self.is_trained = True
                logger.info(f"Model loaded successfully from {self.model_path}")
                return True
            else:
                logger.warning(f"Model file not found at {self.model_path}")
                self._initialize_new_model()
                return False
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self._initialize_new_model()
            return False
    
    def _initialize_new_model(self):
        """Initialize a new model"""
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        self.is_trained = False
        logger.info("New model initialized with 26 parameters")
    
    def save_model(self) -> bool:
        """Save trained model to file"""
        try:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'normal_ranges': self.normal_ranges,
                'conditions': self.conditions
            }
            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)
            logger.info(f"Model saved successfully to {self.model_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
            return False
    
    def preprocess_data(self, data: pd.DataFrame) -> np.ndarray:
        """Preprocess the input data"""
        try:
            # Ensure all 26 features are present
            for feature in self.feature_names:
                if feature not in data.columns:
                    data[feature] = np.nan
            
            # Select only the required features in correct order
            data = data[self.feature_names]
            
            # Fill missing values with median
            data = data.fillna(data.median())
            
            # Scale the features
            if self.is_trained:
                scaled_data = self.scaler.transform(data)
            else:
                scaled_data = self.scaler.fit_transform(data)
            
            return scaled_data
        except Exception as e:
            logger.error(f"Error in data preprocessing: {str(e)}")
            raise
    
    def train(self, X: pd.DataFrame, y: pd.Series, test_size: float = 0.2) -> Dict[str, Any]:
        """Train the model with provided data"""
        try:
            logger.info("Starting model training...")
            
            # Preprocess features
            X_processed = self.preprocess_data(X)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_processed, y, test_size=test_size, random_state=42, stratify=y
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            self.is_trained = True
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Save model
            self.save_model()
            
            results = {
                'accuracy': accuracy,
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'features_used': len(self.feature_names),
                'training_samples': len(X_train),
                'test_samples': len(X_test)
            }
            
            logger.info(f"Model training completed. Accuracy: {accuracy:.4f}")
            return results
            
        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise
    
    def predict(self, blood_data: Dict[str, float]) -> Dict[str, Any]:
        """Predict health condition based on blood test results"""
        try:
            if not self.is_trained:
                return {
                    'error': 'Model not trained',
                    'suggestion': 'Train the model first or load a pre-trained model'
                }
            
            # Convert input to DataFrame
            input_df = pd.DataFrame([blood_data])
            
            # Preprocess data
            processed_data = self.preprocess_data(input_df)
            
            # Make prediction
            prediction = self.model.predict(processed_data)[0]
            probabilities = self.model.predict_proba(processed_data)[0]
            
            # Get confidence score
            confidence = max(probabilities)
            
            # Analyze abnormalities
            abnormalities = self._analyze_abnormalities(blood_data)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(prediction, abnormalities)
            
            return {
                'prediction': prediction,
                'confidence': float(confidence),
                'probabilities': dict(zip(self.model.classes_, probabilities)),
                'abnormalities': abnormalities,
                'recommendations': recommendations,
                'parameters_analyzed': len(self.feature_names)
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            return {
                'error': f'Prediction failed: {str(e)}',
                'prediction': 'UNKNOWN',
                'confidence': 0.0
            }
    
    def _analyze_abnormalities(self, blood_data: Dict[str, float]) -> List[Dict[str, Any]]:
        """Analyze which parameters are outside normal ranges"""
        abnormalities = []
        
        for param, value in blood_data.items():
            if param in self.normal_ranges:
                low, high = self.normal_ranges[param]
                if value < low:
                    abnormalities.append({
                        'parameter': param,
                        'value': value,
                        'normal_range': f"{low}-{high}",
                        'status': 'LOW',
                        'severity': self._calculate_severity(value, low, high, 'LOW')
                    })
                elif value > high:
                    abnormalities.append({
                        'parameter': param,
                        'value': value,
                        'normal_range': f"{low}-{high}",
                        'status': 'HIGH',
                        'severity': self._calculate_severity(value, low, high, 'HIGH')
                    })
        
        return sorted(abnormalities, key=lambda x: x['severity'], reverse=True)
    
    def _calculate_severity(self, value: float, low: float, high: float, status: str) -> str:
        """Calculate severity of abnormality"""
        if status == 'LOW':
            deviation = (low - value) / low
        else:
            deviation = (value - high) / high
        
        if deviation > 0.5:
            return 'HIGH'
        elif deviation > 0.2:
            return 'MODERATE'
        else:
            return 'MILD'
    
    def _generate_recommendations(self, prediction: str, abnormalities: List[Dict]) -> List[str]:
        """Generate health recommendations based on prediction and abnormalities"""
        recommendations = []
        
        # General recommendations based on prediction
        if prediction == 'ANEMIA':
            recommendations.extend([
                "Increase iron-rich foods in diet",
                "Consider iron supplements after consulting doctor",
                "Include Vitamin C to improve iron absorption"
            ])
        elif prediction == 'DIABETES':
            recommendations.extend([
                "Monitor blood sugar regularly",
                "Follow diabetic diet plan",
                "Exercise regularly",
                "Consult endocrinologist"
            ])
        elif prediction == 'LIVER_DISEASE':
            recommendations.extend([
                "Avoid alcohol completely",
                "Reduce fatty foods",
                "Consult gastroenterologist",
                "Monitor liver enzymes regularly"
            ])
        elif prediction == 'KIDNEY_DISEASE':
            recommendations.extend([
                "Reduce protein intake",
                "Monitor blood pressure",
                "Limit salt consumption",
                "Consult nephrologist"
            ])
        
        # Specific recommendations based on abnormalities
        for ab in abnormalities:
            if ab['parameter'] == 'cholesterol' and ab['status'] == 'HIGH':
                recommendations.append("Reduce saturated fats and increase fiber intake")
            elif ab['parameter'] == 'glucose' and ab['status'] == 'HIGH':
                recommendations.append("Reduce sugar and carbohydrate intake")
            elif ab['parameter'] == 'hemoglobin' and ab['status'] == 'LOW':
                recommendations.append("Include more green leafy vegetables and legumes")
        
        # General health recommendations
        recommendations.extend([
            "Maintain regular exercise routine",
            "Stay hydrated with adequate water intake",
            "Get 7-8 hours of quality sleep daily",
            "Manage stress through meditation or yoga"
        ])
        
        return list(set(recommendations))[:6]  # Return top 6 unique recommendations
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the trained model"""
        if not self.is_trained:
            return {}
        
        importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))

# Global model instance
blood_analysis_model = BloodAnalysisModel()