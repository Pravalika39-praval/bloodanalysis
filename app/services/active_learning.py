import logging
import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)

class ActiveLearning:
    def __init__(self, model):
        self.model = model
        self.uncertainty_scores = []
    
    def select_samples_for_labeling(self, unlabeled_data: pd.DataFrame, n_samples: int = 100) -> pd.DataFrame:
        """Select most uncertain samples for manual labeling"""
        if not hasattr(self.model, 'is_trained') or not self.model.is_trained:
            return self._select_diverse_samples(unlabeled_data, n_samples)
        
        uncertainties = self._calculate_uncertainty(unlabeled_data)
        
        unlabeled_data = unlabeled_data.copy()
        unlabeled_data['uncertainty'] = uncertainties
        selected_samples = unlabeled_data.nlargest(n_samples, 'uncertainty')
        
        logger.info(f"Selected {len(selected_samples)} samples for labeling")
        return selected_samples
    
    def _calculate_uncertainty(self, data: pd.DataFrame) -> List[float]:
        """Calculate prediction uncertainty"""
        uncertainties = []
        
        for _, row in data.iterrows():
            try:
                parameters = {k: v for k, v in row.items() 
                            if not pd.isna(v) and k not in ['image_path', 'filename']}
                
                # Get prediction probabilities
                predictions = self.model.predict(parameters)
                if predictions:
                    max_prob = max(prob for _, prob in predictions)
                    uncertainty = 1 - max_prob
                    uncertainties.append(uncertainty)
                else:
                    uncertainties.append(1.0)
                    
            except Exception as e:
                logger.warning(f"Uncertainty calculation error: {e}")
                uncertainties.append(1.0)
        
        return uncertainties
    
    def _select_diverse_samples(self, data: pd.DataFrame, n_samples: int) -> pd.DataFrame:
        """Select diverse samples when no model is available"""
        return data.sample(n=min(n_samples, len(data)), random_state=42)
    
    def update_model_with_new_labels(self, labeled_data: pd.DataFrame, model_save_path: str):
        """Update model with newly labeled data"""
        try:
            logger.info("Updating model with new labeled data")
            # This would retrain the model with new data
            # For now, just log the update
            logger.info(f"Received {len(labeled_data)} new labeled samples")
            
        except Exception as e:
            logger.error(f"Model update error: {e}")