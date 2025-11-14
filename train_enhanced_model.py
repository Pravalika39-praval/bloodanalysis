import argparse
import logging
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import cv2
import pytesseract
from PIL import Image
import re
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('model_training.log')
    ]
)

logger = logging.getLogger(__name__)

class EnhancedBloodAnalysisModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # All 26 parameters in fixed order
        self.parameter_names = [
            'WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT',
            'RDW_SD', 'RDW_CV', 'PDW', 'MPV', 'P_LCR', 'PCT', 'NEUT',
            'LYMPH', 'MONO', 'EO', 'BASO', 'IG', 'NRBCS', 'RETICULOCYTES',
            'IRF', 'LFR', 'MFR', 'HFR'
        ]
        
        # Enhanced parameter patterns with more variations
        self.parameter_patterns = {
            'WBC': [r'WBC', r'White Blood Cells?', r'Leukocytes?', r'White Blood Cell Count', r'White Cells'],
            'RBC': [r'RBC', r'Red Blood Cells?', r'Erythrocytes?', r'Red Blood Cell Count', r'Red Cells'],
            'HGB': [r'HGB', r'Hb', r'Hemoglobin', r'Hemo', r'HbA1c'],
            'HCT': [r'HCT', r'Hematocrit', r'Hct', r'Packed Cell Volume', r'PCV'],
            'MCV': [r'MCV', r'Mean Corpuscular Volume', r'Mean Cell Volume'],
            'MCH': [r'MCH', r'Mean Corpuscular Hemoglobin', r'Mean Cell Hemoglobin'],
            'MCHC': [r'MCHC', r'Mean Corpuscular Hemoglobin Concentration', r'Mean Cell Hb Concentration'],
            'PLT': [r'PLT', r'Platelets?', r'Platelet Count', r'Thrombocytes?'],
            'RDW_SD': [r'RDW-SD', r'RDW SD', r'Red Cell Distribution Width SD'],
            'RDW_CV': [r'RDW-CV', r'RDW CV', r'Red Cell Distribution Width CV', r'RDW'],
            'PDW': [r'PDW', r'Platelet Distribution Width'],
            'MPV': [r'MPV', r'Mean Platelet Volume'],
            'P_LCR': [r'P-LCR', r'PLCR', r'Platelet Large Cell Ratio'],
            'PCT': [r'PCT', r'Plateletcrit'],
            'NEUT': [r'NEUT', r'Neutrophils?', r'Neutrophil Count', r'Neut', r'Granulocytes?'],
            'LYMPH': [r'LYMPH', r'Lymphocytes?', r'Lymphocyte Count', r'Lymph'],
            'MONO': [r'MONO', r'Monocytes?', r'Monocyte Count', r'Mono'],
            'EO': [r'EO', r'Eosinophils?', r'Eosinophil Count', r'Eos'],
            'BASO': [r'BASO', r'Basophils?', r'Basophil Count', r'Baso'],
            'IG': [r'IG', r'Immature Granulocytes?'],
            'NRBCS': [r'NRBC', r'Nucleated RBC', r'Nucleated Red Blood Cells?'],
            'RETICULOCYTES': [r'Reticulocytes?', r'RETIC', r'Reticulocyte Count', r'Retic'],
            'IRF': [r'IRF', r'Immature Reticulocyte Fraction'],
            'LFR': [r'LFR', r'Low Fluorescence Reticulocytes?'],
            'MFR': [r'MFR', r'Medium Fluorescence Reticulocytes?'],
            'HFR': [r'HFR', r'High Fluorescence Reticulocytes?']
        }

        # Normal ranges for validation
        self.normal_ranges = {
            'WBC': (4.5, 10.0), 'RBC': (4.2, 5.4), 'HGB': (12.0, 16.0),
            'HCT': (36.1, 44.3), 'MCV': (80, 100), 'MCH': (27, 31),
            'MCHC': (33, 36), 'PLT': (150, 400), 'RDW_SD': (39, 46),
            'RDW_CV': (11.6, 14.6), 'PDW': (10, 17), 'MPV': (7.5, 11.5),
            'P_LCR': (13, 43), 'PCT': (0.1, 0.5), 'NEUT': (1.5, 8.0),
            'LYMPH': (1.0, 4.0), 'MONO': (0.2, 0.8), 'EO': (0.04, 0.4),
            'BASO': (0.0, 0.2), 'IG': (0.0, 0.05), 'NRBCS': (0, 0),
            'RETICULOCYTES': (0.5, 2.5), 'IRF': (0.48, 27.0),
            'LFR': (87.0, 91.4), 'MFR': (11.0, 18.0), 'HFR': (0.0, 1.7)
        }

    def enhanced_preprocess_image(self, image_path):
        """Enhanced image preprocessing for better OCR"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                logger.warning(f"Could not read image: {image_path}")
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Try multiple preprocessing techniques
            processed_images = []
            
            # 1. Simple threshold
            _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            processed_images.append(thresh1)
            
            # 2. Adaptive threshold
            thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                          cv2.THRESH_BINARY, 11, 2)
            processed_images.append(thresh2)
            
            # 3. Noise removal + threshold
            denoised = cv2.medianBlur(gray, 3)
            _, thresh3 = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            processed_images.append(thresh3)
            
            # 4. Morphological operations to clean image
            kernel = np.ones((1,1), np.uint8)
            opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
            processed_images.append(opening)
            
            return processed_images
            
        except Exception as e:
            logger.error(f"Image preprocessing error for {image_path}: {e}")
            return None

    def extract_text_from_image(self, image_path):
        """Extract text from blood report image with multiple OCR attempts"""
        try:
            logger.info(f"Processing image: {image_path}")
            
            processed_images = self.enhanced_preprocess_image(image_path)
            if not processed_images:
                return ""
            
            # Try different OCR configurations
            ocr_configs = [
                r'--oem 3 --psm 6',      # Uniform block of text
                r'--oem 3 --psm 4',      # Single column of text
                r'--oem 3 --psm 8',      # Single word
                r'--oem 3 --psm 11',     # Sparse text
                r'--oem 3 --psm 12',     # Sparse text with OSD
            ]
            
            best_text = ""
            best_score = 0
            
            for i, processed_img in enumerate(processed_images):
                for config in ocr_configs:
                    try:
                        text = pytesseract.image_to_string(processed_img, config=config)
                        
                        # Score text quality (more alphanumeric = better)
                        alpha_count = len(re.findall(r'[a-zA-Z0-9]', text))
                        total_chars = len(text.strip())
                        
                        if total_chars > 0:
                            score = alpha_count / total_chars
                            
                            # Prefer longer texts with good quality
                            if score > 0.3 and len(text) > len(best_text):
                                best_text = text
                                best_score = score
                                
                    except Exception as e:
                        logger.debug(f"OCR config {config} failed for image {i}: {e}")
                        continue
            
            if best_text:
                logger.info(f"✅ Extracted {len(best_text)} characters from {os.path.basename(image_path)}")
                return best_text
            else:
                logger.warning(f"❌ No text extracted from {os.path.basename(image_path)}")
                return ""
            
        except Exception as e:
            logger.error(f"Error extracting text from {image_path}: {e}")
            return ""

    def extract_parameters_from_text(self, text):
        """Enhanced parameter extraction with better pattern matching"""
        parameters = {}
        
        if not text or len(text.strip()) < 20:
            return parameters
            
        lines = text.split('\n')
        
        for param_name, patterns in self.parameter_patterns.items():
            param_value = None
            
            for pattern in patterns:
                for i, line in enumerate(lines):
                    # More flexible matching
                    if re.search(pattern, line, re.IGNORECASE):
                        # Look for value in format: "Parameter: 12.34" or "12.34" near parameter
                        value = self._extract_number_enhanced(line, lines, i)
                        if value is not None:
                            param_value = value
                            break
                        
                if param_value is not None:
                    break
            
            if param_value is not None:
                parameters[param_name] = param_value
                logger.debug(f"Extracted {param_name}: {param_value}")
        
        logger.info(f"Extracted {len(parameters)} parameters from text")
        return parameters

    def _extract_number_enhanced(self, current_line, all_lines, current_index):
        """Enhanced number extraction from text"""
        # Check current line
        value = self._extract_number_from_text(current_line)
        if value is not None:
            return value
        
        # Check surrounding lines (2 lines before and after)
        search_range = range(max(0, current_index-2), min(len(all_lines), current_index+3))
        
        for i in search_range:
            if i != current_index:  # Don't check the same line again
                value = self._extract_number_from_text(all_lines[i])
                if value is not None:
                    return value
        
        return None

    def _extract_number_from_text(self, text):
        """Extract numerical value from text"""
        try:
            # Remove commas and special characters, keep dots for decimals
            clean_text = re.sub(r'[^\d.]', ' ', text)
            
            # Look for numbers with possible decimal points
            numbers = re.findall(r'\d+\.\d+|\d+', clean_text)
            
            for num in numbers:
                try:
                    value = float(num)
                    # Validate reasonable range for blood parameters
                    if 0.01 <= value <= 1000:  # Wider range for blood parameters
                        return value
                except ValueError:
                    continue
                    
        except Exception:
            pass
            
        return None

    def generate_synthetic_data(self, num_samples=1000):
        """Generate synthetic training data when real data extraction fails"""
        logger.info(f"Generating {num_samples} synthetic blood reports for training...")
        
        features_list = []
        labels_list = []
        
        # Disease patterns for synthetic data
        disease_patterns = {
            'Normal': {
                'WBC': (4.5, 10.0), 'RBC': (4.2, 5.4), 'HGB': (12.0, 16.0),
                'HCT': (36.1, 44.3), 'PLT': (150, 400)
            },
            'Iron Deficiency Anemia': {
                'HGB': (8.0, 11.9), 'MCV': (60.0, 79.9), 'MCH': (20.0, 26.9),
                'MCHC': (30.0, 32.9), 'RDW_CV': (15.0, 20.0)
            },
            'Vitamin B12 Deficiency': {
                'HGB': (8.0, 11.9), 'MCV': (100.1, 120.0), 'MCH': (31.1, 35.0),
                'RDW_CV': (15.0, 20.0)
            },
            'Thrombocytopenia': {
                'PLT': (50.0, 149.9), 'MPV': (11.6, 15.0)
            },
            'Leukocytosis': {
                'WBC': (10.1, 30.0), 'NEUT': (8.1, 15.0)
            }
        }
        
        np.random.seed(42)
        
        for _ in range(num_samples):
            # Choose a random disease or normal
            disease = np.random.choice(list(disease_patterns.keys()))
            pattern = disease_patterns[disease]
            
            features = np.full(26, 0.0)
            
            for i, param_name in enumerate(self.parameter_names):
                if param_name in pattern:
                    # Generate value within disease range
                    min_val, max_val = pattern[param_name]
                    value = np.random.uniform(min_val, max_val)
                else:
                    # Generate normal value
                    if param_name in self.normal_ranges:
                        min_val, max_val = self.normal_ranges[param_name]
                        value = np.random.uniform(min_val, max_val)
                    else:
                        value = 0.0
                
                features[i] = value
            
            features_list.append(features)
            labels_list.append(disease)
        
        return np.array(features_list), labels_list

    def prepare_features(self, parameters):
        """Prepare feature vector with all 26 parameters"""
        feature_vector = np.full(26, 0.0)
        
        for i, param_name in enumerate(self.parameter_names):
            if param_name in parameters:
                feature_vector[i] = parameters[param_name]
            else:
                # Impute missing values with normal range median
                if param_name in self.normal_ranges:
                    min_val, max_val = self.normal_ranges[param_name]
                    feature_vector[i] = (min_val + max_val) / 2
        
        return feature_vector

    def process_dataset(self, dataset_path):
        """Process dataset with fallback to synthetic data"""
        features_list = []
        labels_list = []
        successful_extractions = 0
        
        # Try to process real images first
        if os.path.exists(dataset_path):
            logger.info(f"Attempting to process real images from: {dataset_path}")
            
            # Find all image files
            supported_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif']
            image_files = []
            
            for root, dirs, files in os.walk(dataset_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in supported_extensions):
                        image_files.append(os.path.join(root, file))
            
            logger.info(f"Found {len(image_files)} image files")
            
            for i, image_path in enumerate(image_files):
                if i % 10 == 0:
                    logger.info(f"Processed {i}/{len(image_files)} images...")
                
                try:
                    # Extract text and parameters
                    text = self.extract_text_from_image(image_path)
                    parameters = self.extract_parameters_from_text(text)
                    
                    if len(parameters) >= 3:  # Require at least 3 parameters
                        # Generate synthetic label based on parameters
                        label = self._generate_label_from_parameters(parameters)
                        
                        # Prepare features
                        features = self.prepare_features(parameters)
                        
                        features_list.append(features)
                        labels_list.append(label)
                        successful_extractions += 1
                        
                except Exception as e:
                    logger.warning(f"Failed to process {image_path}: {e}")
                    continue
        
        # If no real data extracted, use synthetic data
        if successful_extractions < 50:  # If less than 50 successful extractions
            logger.warning(f"Only {successful_extractions} real samples extracted. Using synthetic data...")
            synthetic_features, synthetic_labels = self.generate_synthetic_data(500)
            features_list.extend(synthetic_features)
            labels_list.extend(synthetic_labels)
            logger.info(f"Added {len(synthetic_features)} synthetic samples")
        
        logger.info(f"Total training samples: {len(features_list)}")
        return np.array(features_list), labels_list

    def _generate_label_from_parameters(self, parameters):
        """Generate label based on parameter patterns"""
        hgb = parameters.get('HGB')
        mcv = parameters.get('MCV')
        plt = parameters.get('PLT')
        wbc = parameters.get('WBC')
        
        # Simple rule-based labeling
        if hgb and mcv:
            if hgb < 12 and mcv < 80:
                return 'Iron Deficiency Anemia'
            elif hgb < 12 and mcv > 100:
                return 'Vitamin B12 Deficiency'
        
        if plt and plt < 150:
            return 'Thrombocytopenia'
        
        if wbc and wbc > 10:
            return 'Leukocytosis'
        
        if wbc and wbc < 4.5:
            return 'Leukopenia'
        
        return 'Normal'

    def train(self, dataset_path, model_save_path):
        """Train the model with real or synthetic data"""
        try:
            # Process dataset
            logger.info("Processing dataset...")
            X, y = self.process_dataset(dataset_path)
            
            if len(X) == 0:
                logger.error("No training data available!")
                return False
            
            logger.info(f"Training on {len(X)} samples with {len(set(y))} classes")
            logger.info(f"Class distribution: {dict(pd.Series(y).value_counts())}")
            
            # Encode labels
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
            )
            
            logger.info(f"Training set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
            
            # Scale features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Train Random Forest model
            self.model = RandomForestClassifier(
                n_estimators=100,  # Reduced for faster training
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            )
            
            logger.info("Training Random Forest model...")
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            train_score = accuracy_score(y_train, self.model.predict(X_train_scaled))
            test_score = accuracy_score(y_test, self.model.predict(X_test_scaled))
            
            logger.info(f"Training accuracy: {train_score:.3f}")
            logger.info(f"Test accuracy: {test_score:.3f}")
            
            # Save model
            self.save_model(model_save_path)
            self.is_trained = True
            
            # Print feature importance
            self._print_feature_importance()
            
            return True
            
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False

    def _print_feature_importance(self):
        """Print feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
            feature_imp = list(zip(self.parameter_names, importances))
            feature_imp.sort(key=lambda x: x[1], reverse=True)
            
            logger.info("\n📊 Top 10 Most Important Features:")
            for i, (feature, importance) in enumerate(feature_imp[:10], 1):
                logger.info(f"  {i:2d}. {feature:15s}: {importance:.3f}")

    def save_model(self, model_path):
        """Save trained model"""
        try:
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            model_data = {
                'model': self.model,
                'scaler': self.scaler,
                'label_encoder': self.label_encoder,
                'parameter_names': self.parameter_names,
                'is_trained': self.is_trained
            }
            joblib.dump(model_data, model_path)
            logger.info(f"✅ Model saved to {model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")

def main():
    parser = argparse.ArgumentParser(description='Train enhanced blood analysis model')
    parser.add_argument('--dataset_path', type=str, 
                       default=r'C:\Users\ardha\Downloads\combine',
                       help='Path to dataset directory containing blood report images')
    parser.add_argument('--model_save_path', type=str, 
                       default='ml_models/enhanced_blood_model.pkl',
                       help='Path to save trained model')
    
    args = parser.parse_args()
    
    print("🩸 Blood Analysis Model Training")
    print("=" * 50)
    
    # Check if dataset path exists
    if not os.path.exists(args.dataset_path):
        print(f"⚠️  Dataset path does not exist: {args.dataset_path}")
        print("Will use synthetic data for training...")
    
    print(f"💾 Model will be saved to: {args.model_save_path}")
    print("\nStarting training process...")
    
    # Train model
    model = EnhancedBloodAnalysisModel()
    success = model.train(args.dataset_path, args.model_save_path)
    
    if success:
        print("\n🎉 Model training completed successfully!")
        print("\nThe model will now:")
        print("• Use real data if OCR works")
        print("• Fall back to synthetic data if OCR fails") 
        print("• Handle all 26 blood parameters")
        print("• Be ready for API use")
    else:
        print("\n❌ Model training failed!")
        print("Check the logs for more details.")

if __name__ == "__main__":
    main()