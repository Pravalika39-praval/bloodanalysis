import re
import logging
from typing import Dict, Optional, List, Any
import spacy
from datetime import datetime

logger = logging.getLogger(__name__)

class NLPExtractor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully")
        except OSError:
            logger.warning("spaCy model not found, using basic extraction only")
            self.nlp = None
        
        # Complete parameter patterns for all 26 parameters
        self.parameter_patterns = {
            'WBC': [r'WBC', r'White Blood Cells?', r'Leukocytes?', r'White Blood Cell Count'],
            'RBC': [r'RBC', r'Red Blood Cells?', r'Erythrocytes?', r'Red Blood Cell Count'],
            'HGB': [r'HGB', r'Hb', r'Hemoglobin'],
            'HCT': [r'HCT', r'Hematocrit'],
            'MCV': [r'MCV', r'Mean Corpuscular Volume'],
            'MCH': [r'MCH', r'Mean Corpuscular Hemoglobin'],
            'MCHC': [r'MCHC', r'Mean Corpuscular Hemoglobin Concentration'],
            'PLT': [r'PLT', r'Platelets?', r'Platelet Count'],
            'RDW_SD': [r'RDW-SD', r'RDW SD', r'Red Cell Distribution Width SD'],
            'RDW_CV': [r'RDW-CV', r'RDW CV', r'Red Cell Distribution Width CV'],
            'PDW': [r'PDW', r'Platelet Distribution Width'],
            'MPV': [r'MPV', r'Mean Platelet Volume'],
            'P_LCR': [r'P-LCR', r'PLCR', r'Platelet Large Cell Ratio'],
            'PCT': [r'PCT', r'Plateletcrit'],
            'NEUT': [r'NEUT', r'Neutrophils?', r'Neutrophil Count'],
            'LYMPH': [r'LYMPH', r'Lymphocytes?', r'Lymphocyte Count'],
            'MONO': [r'MONO', r'Monocytes?', r'Monocyte Count'],
            'EO': [r'EO', r'Eosinophils?', r'Eosinophil Count'],
            'BASO': [r'BASO', r'Basophils?', r'Basophil Count'],
            'IG': [r'IG', r'Immature Granulocytes?'],
            'NRBCS': [r'NRBC', r'Nucleated RBC', r'Nucleated Red Blood Cells?'],
            'RETICULOCYTES': [r'Reticulocytes?', r'RETIC', r'Reticulocyte Count'],
            'IRF': [r'IRF', r'Immature Reticulocyte Fraction'],
            'LFR': [r'LFR', r'Low Fluorescence Reticulocytes?'],
            'MFR': [r'MFR', r'Medium Fluorescence Reticulocytes?'],
            'HFR': [r'HFR', r'High Fluorescence Reticulocytes?']
        }
        
        # Unit patterns
        self.unit_patterns = [
            r'×10⁹/L', r'×10\^9/L', r'10\^9/L', r'10\*\*9/L',
            r'×10⁶/µL', r'×10\^6/µL', r'10\^6/µL', r'10\*\*6/µL',
            r'g/dL', r'g/L', r'gm/dL',
            r'%', r'percent', r'percentage',
            r'fL', r'femtoliter',
            r'pg', r'picogram'
        ]

    def extract_parameters(self, text: str) -> Dict[str, Optional[float]]:
        """Extract all 26 blood parameters from text using NLP and pattern matching"""
        parameters = {}
        
        # Split text into lines for processing
        lines = text.split('\n')
        
        for param_name, patterns in self.parameter_patterns.items():
            param_value = self._extract_parameter_value(lines, patterns)
            if param_value is not None:
                parameters[param_name] = param_value
                logger.debug(f"Extracted {param_name}: {param_value}")
        
        logger.info(f"Extracted {len(parameters)} parameters from text")
        return parameters
    
    def _extract_parameter_value(self, lines: List[str], patterns: List[str]) -> Optional[float]:
        """Extract parameter value using multiple patterns"""
        for pattern in patterns:
            for i, line in enumerate(lines):
                # Case insensitive search
                if re.search(pattern, line, re.IGNORECASE):
                    # Look for numerical values in the line and surrounding lines
                    value = self._extract_numerical_value(line)
                    if value is not None:
                        return value
                    
                    # Check next line if value not found in same line
                    if i + 1 < len(lines):
                        next_line = lines[i + 1]
                        value = self._extract_numerical_value(next_line)
                        if value is not None:
                            return value
        
        return None
    
    def _extract_numerical_value(self, text: str) -> Optional[float]:
        """Extract numerical value from text, handling various formats"""
        # Remove commas from numbers
        text = text.replace(',', '')
        
        # Look for patterns like: "Parameter: 12.34 unit" or "12.34 (unit)"
        patterns = [
            r'(\d+\.\d+)',  # Decimal numbers
            r'(\d+)',       # Whole numbers
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                # Take the first match that looks like a reasonable blood parameter value
                for match in matches:
                    try:
                        value = float(match)
                        # Filter out unlikely values (e.g., dates, page numbers)
                        if self._is_reasonable_blood_value(value):
                            return value
                    except ValueError:
                        continue
        
        return None
    
    def _is_reasonable_blood_value(self, value: float) -> bool:
        """Check if value is within reasonable range for blood parameters"""
        # Most blood parameters fall within these ranges
        if 0.001 <= value <= 1000:
            return True
        return False
    
    def clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common OCR artifacts
        artifacts = [
            r'', r'•', r'·', r'■', r'□', r'●', r'○',  # Bullet characters
            r'Page \d+', r'Page\d+',  # Page numbers
            r'\x0c', r'\f',  # Form feed
            r'http[s]?://\S+',  # URLs
            r'www\.\S+',  # Websites
        ]
        
        for artifact in artifacts:
            text = re.sub(artifact, '', text)
        
        return text.strip()
    
    def validate_parameters(self, parameters: Dict[str, float]) -> Dict[str, float]:
        """Validate extracted parameters for reasonable ranges"""
        validated = {}
        
        # Reasonable ranges for all 26 parameters
        reasonable_ranges = {
            'WBC': (1.0, 50.0),
            'RBC': (2.0, 8.0),
            'HGB': (5.0, 20.0),
            'HCT': (20.0, 60.0),
            'MCV': (60.0, 120.0),
            'MCH': (20.0, 40.0),
            'MCHC': (30.0, 38.0),
            'PLT': (50.0, 600.0),
            'RDW_SD': (35.0, 60.0),
            'RDW_CV': (10.0, 20.0),
            'PDW': (8.0, 25.0),
            'MPV': (6.0, 15.0),
            'P_LCR': (10.0, 50.0),
            'PCT': (0.05, 0.7),
            'NEUT': (0.5, 15.0),
            'LYMPH': (0.5, 10.0),
            'MONO': (0.1, 1.5),
            'EO': (0.02, 0.8),
            'BASO': (0.0, 0.5),
            'IG': (0.0, 0.1),
            'NRBCS': (0.0, 5.0),
            'RETICULOCYTES': (0.1, 5.0),
            'IRF': (0.3, 35.0),
            'LFR': (80.0, 95.0),
            'MFR': (8.0, 25.0),
            'HFR': (0.0, 3.0)
        }
        
        for param, value in parameters.items():
            if param in reasonable_ranges:
                min_val, max_val = reasonable_ranges[param]
                if min_val <= value <= max_val:
                    validated[param] = value
                else:
                    logger.warning(f"Parameter {param} value {value} outside reasonable range ({min_val}-{max_val})")
            else:
                validated[param] = value
        
        return validated