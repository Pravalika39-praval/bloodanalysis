import os
import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional
import json
from .ocr_service import OCRService
from .nlp_extractor import NLPExtractor

logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self):
        self.ocr_service = OCRService()
        self.nlp_extractor = NLPExtractor()
        self.extracted_data = []
    
    def process_dataset(self, dataset_path: str, output_csv: str = None) -> pd.DataFrame:
        """Process all images in dataset and extract features"""
        logger.info(f"Processing dataset from {dataset_path}")
        
        image_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith('.png'):
                    image_files.append(os.path.join(root, file))
        
        logger.info(f"Found {len(image_files)} PNG images")
        
        results = []
        for i, image_path in enumerate(image_files):
            if i % 100 == 0:
                logger.info(f"Processed {i}/{len(image_files)} images")
            
            try:
                # Extract parameters from image
                parameters = self.extract_parameters_from_image(image_path)
                
                if parameters:
                    result = {
                        'image_path': image_path,
                        'filename': os.path.basename(image_path),
                        **parameters
                    }
                    results.append(result)
                    
            except Exception as e:
                logger.warning(f"Failed to process {image_path}: {e}")
                continue
        
        # Create DataFrame
        df = pd.DataFrame(results)
        
        # Save to CSV if requested
        if output_csv:
            df.to_csv(output_csv, index=False)
            logger.info(f"Extracted data saved to {output_csv}")
        
        logger.info(f"Successfully processed {len(df)} images")
        return df
    
    def extract_parameters_from_image(self, image_path: str) -> Dict[str, float]:
        """Extract blood parameters from PNG image"""
        try:
            # Extract text from image
            extracted_text = self.ocr_service.extract_text_from_image(image_path)
            
            if not extracted_text or len(extracted_text.strip()) < 10:
                return {}
            
            # Clean and process text
            cleaned_text = self.nlp_extractor.clean_extracted_text(extracted_text)
            
            # Extract parameters using NLP
            parameters = self.nlp_extractor.extract_parameters(cleaned_text)
            validated_parameters = self.nlp_extractor.validate_parameters(parameters)
            
            # Add metadata
            validated_parameters['extracted_text_length'] = len(cleaned_text)
            validated_parameters['parameters_found'] = len(validated_parameters)
            
            return validated_parameters
            
        except Exception as e:
            logger.error(f"Error extracting parameters from {image_path}: {e}")
            return {}
    
    def generate_labels_automatically(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate initial labels based on parameter patterns"""
        logger.info("Generating automatic labels based on parameter patterns...")
        
        labels = []
        confidence_scores = []
        
        for _, row in df.iterrows():
            label, confidence = self._predict_label_from_parameters(row.to_dict())
            labels.append(label)
            confidence_scores.append(confidence)
        
        df['auto_label'] = labels
        df['confidence'] = confidence_scores
        df['needs_review'] = df['confidence'] < 0.7  # Flag low-confidence predictions for manual review
        
        logger.info("Automatic labeling completed")
        return df
    
    def _predict_label_from_parameters(self, parameters: Dict) -> Tuple[str, float]:
        """Predict disease label based on parameter patterns"""
        # Rule-based labeling for initial training data
        hgb = parameters.get('HGB')
        mcv = parameters.get('MCV')
        plt = parameters.get('PLT')
        wbc = parameters.get('WBC')
        rbc = parameters.get('RBC')
        
        # Iron Deficiency Anemia
        if hgb and mcv and hgb < 12 and mcv < 80:
            return 'Iron Deficiency Anemia', 0.85
        
        # Vitamin B12 Deficiency
        if hgb and mcv and hgb < 12 and mcv > 100:
            return 'Vitamin B12 Deficiency', 0.80
        
        # Thrombocytopenia
        if plt and plt < 150:
            return 'Thrombocytopenia', 0.90
        
        # Leukocytosis
        if wbc and wbc > 10:
            return 'Leukocytosis', 0.75
        
        # Leukopenia
        if wbc and wbc < 4.5:
            return 'Leukopenia', 0.80
        
        # Polycythemia
        if rbc and rbc > 5.4:
            return 'Polycythemia', 0.70
        
        # Normal (if most parameters are within normal range)
        abnormal_count = sum(1 for param, value in parameters.items() 
                           if self._is_abnormal_parameter(param, value))
        if abnormal_count <= 1:
            return 'Normal', 0.70
        else:
            return 'Multiple Conditions', 0.60
    
    def _is_abnormal_parameter(self, param: str, value: float) -> bool:
        """Check if parameter is abnormal"""
        from .blood_config import NORMAL_RANGES
        
        if param in NORMAL_RANGES and param not in ['extracted_text_length', 'parameters_found']:
            normal_min = NORMAL_RANGES[param]['min']
            normal_max = NORMAL_RANGES[param]['max']
            return value < normal_min or value > normal_max
        
        return False
    
    def create_labeling_interface_data(self, df: pd.DataFrame, output_file: str):
        """Create data for manual labeling interface"""
        labeling_data = []
        
        for _, row in df.iterrows():
            item = {
                'image_path': row['image_path'],
                'filename': row['filename'],
                'extracted_parameters': {k: v for k, v in row.items() 
                                       if k not in ['image_path', 'filename', 'auto_label', 'confidence', 'needs_review'] 
                                       and not pd.isna(v)},
                'auto_label': row.get('auto_label', 'Unknown'),
                'confidence': row.get('confidence', 0),
                'needs_review': row.get('needs_review', True),
                'manual_label': '',  # To be filled by human labeler
                'reviewed': False
            }
            labeling_data.append(item)
        
        with open(output_file, 'w') as f:
            json.dump(labeling_data, f, indent=2)
        
        logger.info(f"Labeling interface data saved to {output_file}")
        return labeling_data