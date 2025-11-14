from typing import Dict, Any

# Normal ranges for ALL 26 blood parameters
NORMAL_RANGES: Dict[str, Dict[str, Any]] = {
    'WBC': {'min': 4.5, 'max': 10.0, 'unit': '×10⁹/L', 'critical_low': 2.0, 'critical_high': 30.0},
    'RBC': {'min': 4.2, 'max': 5.4, 'unit': '×10⁶/µL', 'critical_low': 3.0, 'critical_high': 6.0},
    'HGB': {'min': 12.0, 'max': 16.0, 'unit': 'g/dL', 'critical_low': 8.0, 'critical_high': 18.0},
    'HCT': {'min': 36.1, 'max': 44.3, 'unit': '%', 'critical_low': 30.0, 'critical_high': 50.0},
    'MCV': {'min': 80, 'max': 100, 'unit': 'fL', 'critical_low': 70, 'critical_high': 110},
    'MCH': {'min': 27, 'max': 31, 'unit': 'pg', 'critical_low': 20, 'critical_high': 35},
    'MCHC': {'min': 33, 'max': 36, 'unit': 'g/dL', 'critical_low': 30, 'critical_high': 38},
    'PLT': {'min': 150, 'max': 400, 'unit': '×10³/µL', 'critical_low': 50, 'critical_high': 600},
    'RDW_SD': {'min': 39, 'max': 46, 'unit': 'fL', 'critical_low': 35, 'critical_high': 60},
    'RDW_CV': {'min': 11.6, 'max': 14.6, 'unit': '%', 'critical_low': 10, 'critical_high': 20},
    'PDW': {'min': 10, 'max': 17, 'unit': 'fL', 'critical_low': 8, 'critical_high': 25},
    'MPV': {'min': 7.5, 'max': 11.5, 'unit': 'fL', 'critical_low': 6, 'critical_high': 15},
    'P_LCR': {'min': 13, 'max': 43, 'unit': '%', 'critical_low': 10, 'critical_high': 50},
    'PCT': {'min': 0.1, 'max': 0.5, 'unit': '%', 'critical_low': 0.05, 'critical_high': 0.7},
    'NEUT': {'min': 1.5, 'max': 8.0, 'unit': '×10⁹/L', 'critical_low': 1.0, 'critical_high': 12.0},
    'LYMPH': {'min': 1.0, 'max': 4.0, 'unit': '×10⁹/L', 'critical_low': 0.5, 'critical_high': 6.0},
    'MONO': {'min': 0.2, 'max': 0.8, 'unit': '×10⁹/L', 'critical_low': 0.1, 'critical_high': 1.5},
    'EO': {'min': 0.04, 'max': 0.4, 'unit': '×10⁹/L', 'critical_low': 0.02, 'critical_high': 0.8},
    'BASO': {'min': 0.0, 'max': 0.2, 'unit': '×10⁹/L', 'critical_low': 0.0, 'critical_high': 0.5},
    'IG': {'min': 0.0, 'max': 0.05, 'unit': '×10⁹/L', 'critical_low': 0.0, 'critical_high': 0.1},
    'NRBCS': {'min': 0, 'max': 0, 'unit': '/100 WBC', 'critical_low': 0, 'critical_high': 5},
    'RETICULOCYTES': {'min': 0.5, 'max': 2.5, 'unit': '%', 'critical_low': 0.1, 'critical_high': 5.0},
    'IRF': {'min': 0.48, 'max': 27.0, 'unit': '%', 'critical_low': 0.3, 'critical_high': 35.0},
    'LFR': {'min': 87.0, 'max': 91.4, 'unit': '%', 'critical_low': 80.0, 'critical_high': 95.0},
    'MFR': {'min': 11.0, 'max': 18.0, 'unit': '%', 'critical_low': 8.0, 'critical_high': 25.0},
    'HFR': {'min': 0.0, 'max': 1.7, 'unit': '%', 'critical_low': 0.0, 'critical_high': 3.0}
}

# Disease patterns using ALL relevant parameters
DISEASE_PATTERNS = {
    'Iron Deficiency Anemia': {
        'parameters': ['HGB', 'MCV', 'MCH', 'MCHC', 'RDW_CV', 'RETICULOCYTES'],
        'pattern': {'HGB': 'low', 'MCV': 'low', 'MCH': 'low', 'MCHC': 'low', 'RDW_CV': 'high', 'RETICULOCYTES': 'normal'},
        'weight': 0.9
    },
    'Vitamin B12 Deficiency': {
        'parameters': ['HGB', 'MCV', 'MCH', 'RDW_CV', 'RETICULOCYTES'],
        'pattern': {'HGB': 'low', 'MCV': 'high', 'MCH': 'high', 'RDW_CV': 'high', 'RETICULOCYTES': 'low'},
        'weight': 0.85
    },
    'Thrombocytopenia': {
        'parameters': ['PLT', 'MPV', 'PCT', 'PDW'],
        'pattern': {'PLT': 'low', 'MPV': 'high', 'PCT': 'low', 'PDW': 'high'},
        'weight': 0.95
    },
    'Leukocytosis': {
        'parameters': ['WBC', 'NEUT', 'LYMPH', 'MONO'],
        'pattern': {'WBC': 'high'},
        'weight': 0.8
    },
    'Leukopenia': {
        'parameters': ['WBC', 'NEUT', 'LYMPH', 'MONO'],
        'pattern': {'WBC': 'low'},
        'weight': 0.85
    },
    'Neutrophilia': {
        'parameters': ['NEUT', 'WBC', 'LYMPH'],
        'pattern': {'NEUT': 'high', 'WBC': 'high', 'LYMPH': 'normal'},
        'weight': 0.75
    },
    'Neutropenia': {
        'parameters': ['NEUT', 'WBC'],
        'pattern': {'NEUT': 'low', 'WBC': 'low'},
        'weight': 0.8
    },
    'Lymphocytosis': {
        'parameters': ['LYMPH', 'WBC', 'NEUT'],
        'pattern': {'LYMPH': 'high', 'WBC': 'high', 'NEUT': 'normal'},
        'weight': 0.7
    },
    'Lymphopenia': {
        'parameters': ['LYMPH', 'WBC'],
        'pattern': {'LYMPH': 'low', 'WBC': 'low'},
        'weight': 0.75
    },
    'Infection': {
        'parameters': ['WBC', 'NEUT', 'LYMPH', 'CRP'],
        'pattern': {'WBC': 'high', 'NEUT': 'high'},
        'weight': 0.7
    },
    'Inflammation': {
        'parameters': ['WBC', 'NEUT', 'MONO'],
        'pattern': {'WBC': 'high', 'NEUT': 'high'},
        'weight': 0.65
    },
    'Polycythemia': {
        'parameters': ['RBC', 'HGB', 'HCT', 'RETICULOCYTES'],
        'pattern': {'RBC': 'high', 'HGB': 'high', 'HCT': 'high', 'RETICULOCYTES': 'normal'},
        'weight': 0.8
    },
    'Bone Marrow Stress': {
        'parameters': ['NRBCS', 'RETICULOCYTES', 'IRF', 'HFR'],
        'pattern': {'NRBCS': 'high', 'RETICULOCYTES': 'high', 'IRF': 'high', 'HFR': 'high'},
        'weight': 0.9
    },
    'Hemolytic Anemia': {
        'parameters': ['HGB', 'RETICULOCYTES', 'LDH', 'BILIRUBIN'],
        'pattern': {'HGB': 'low', 'RETICULOCYTES': 'high'},
        'weight': 0.8
    }
}

SEVERITY_LEVELS = {
    'Normal': (0, 0.2),
    'Low Risk': (0.2, 0.4),
    'Medium Risk': (0.4, 0.6),
    'High Risk': (0.6, 0.8),
    'Critical': (0.8, 1.0)
}

# All 26 parameters in fixed order for ML model
ALL_PARAMETERS = [
    'WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT',
    'RDW_SD', 'RDW_CV', 'PDW', 'MPV', 'P_LCR', 'PCT', 'NEUT',
    'LYMPH', 'MONO', 'EO', 'BASO', 'IG', 'NRBCS', 'RETICULOCYTES',
    'IRF', 'LFR', 'MFR', 'HFR'
]