import logging
from typing import List, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class RecommendationCategory(Enum):
    DIET = "Diet"
    EXERCISE = "Exercise"
    LIFESTYLE = "Lifestyle"
    MEDICAL = "Medical"

class RecommendationTemplate:
    def __init__(self, category: str, text: str, why: str, purpose: str, duration: int, tips: List[str]):
        self.category = category
        self.recommendation_text = text
        self.why = why
        self.purpose = purpose
        self.base_duration = duration
        self.tips = tips

class RecommendationEngine:
    def __init__(self):
        self.disease_recommendations = self._initialize_recommendations()
    
    def _initialize_recommendations(self) -> Dict[str, List[Dict]]:
        """Initialize all disease-specific recommendations"""
        return {
            'Iron Deficiency Anemia': [
                {
                    'category': 'Diet',
                    'recommendation_text': 'Increase iron-rich foods: red meat, spinach, lentils, fortified cereals',
                    'why': 'Low hemoglobin levels indicate iron deficiency',
                    'purpose': 'Boost iron levels and improve oxygen transport',
                    'base_duration': 12,
                    'tips': ['Combine with Vitamin C for better absorption', 'Avoid tea/coffee with meals']
                },
                {
                    'category': 'Medical',
                    'recommendation_text': 'Consult doctor for iron supplements',
                    'why': 'Diet alone may not be sufficient',
                    'purpose': 'Rapidly increase iron stores',
                    'base_duration': 8,
                    'tips': ['Take supplements as prescribed', 'Monitor for side effects']
                }
            ],
            'Vitamin B12 Deficiency': [
                {
                    'category': 'Diet',
                    'recommendation_text': 'Consume B12-rich foods: eggs, fish, dairy, fortified foods',
                    'why': 'Low B12 affects nerve function and red blood cell production',
                    'purpose': 'Restore B12 levels and prevent nerve damage',
                    'base_duration': 16,
                    'tips': ['Include animal products in diet', 'Consider fortified foods if vegetarian']
                }
            ],
            'Thrombocytopenia': [
                {
                    'category': 'Lifestyle',
                    'recommendation_text': 'Avoid activities that may cause bleeding or bruising',
                    'why': 'Low platelet count increases bleeding risk',
                    'purpose': 'Prevent bleeding complications',
                    'base_duration': 12,
                    'tips': ['Use soft-bristle toothbrush', 'Avoid contact sports']
                }
            ],
            'Leukocytosis': [
                {
                    'category': 'Medical',
                    'recommendation_text': 'Consult doctor immediately for infection screening',
                    'why': 'High white blood cells may indicate infection',
                    'purpose': 'Identify and treat underlying cause',
                    'base_duration': 2,
                    'tips': ['Monitor for fever', 'Get prescribed tests done']
                }
            ],
            'Normal': [
                {
                    'category': 'Lifestyle',
                    'recommendation_text': 'Maintain balanced diet and regular exercise',
                    'why': 'Your blood parameters are within normal range',
                    'purpose': 'Maintain good health',
                    'base_duration': 52,
                    'tips': ['Eat variety of fruits and vegetables', 'Exercise 30 minutes daily']
                }
            ]
        }
    
    def generate_recommendations(self, disease_predictions: List[Dict], parameters: Dict[str, float]) -> List[Dict[str, Any]]:
        """Generate personalized recommendations based on disease predictions"""
        recommendations = []
        
        # Add disease-specific recommendations
        for disease in disease_predictions:
            disease_name = disease['disease_name']
            if disease_name in self.disease_recommendations:
                for template in self.disease_recommendations[disease_name]:
                    recommendation = {
                        'category': template['category'],
                        'recommendation_text': template['recommendation_text'],
                        'why': template['why'],
                        'purpose': template['purpose'],
                        'duration_weeks': self._calculate_duration(template['base_duration'], disease['probability']),
                        'priority_level': self._get_priority_level(template['category'], disease['probability']),
                        'disease_related': disease_name
                    }
                    recommendations.append(recommendation)
        
        # If no specific recommendations, add general health tips
        if not recommendations:
            for template in self.disease_recommendations['Normal']:
                recommendations.append({
                    'category': template['category'],
                    'recommendation_text': template['recommendation_text'],
                    'why': template['why'],
                    'purpose': template['purpose'],
                    'duration_weeks': template['base_duration'],
                    'priority_level': 'Low',
                    'disease_related': 'General Health'
                })
        
        # Sort by priority and return top 8
        return sorted(recommendations, key=lambda x: self._priority_score(x['priority_level']))[:8]
    
    def _calculate_duration(self, base_duration: int, probability: float) -> int:
        """Calculate duration based on disease probability"""
        if probability > 0.8:
            return base_duration
        elif probability > 0.5:
            return int(base_duration * 0.75)
        else:
            return int(base_duration * 0.5)
    
    def _get_priority_level(self, category: str, probability: float) -> str:
        """Get priority level based on category and probability"""
        if category == 'Medical' or probability > 0.8:
            return 'High'
        elif category == 'Diet' or probability > 0.5:
            return 'Medium'
        else:
            return 'Low'
    
    def _priority_score(self, priority: str) -> int:
        """Convert priority to numerical score for sorting"""
        priority_scores = {'High': 0, 'Medium': 1, 'Low': 2}
        return priority_scores.get(priority, 3)