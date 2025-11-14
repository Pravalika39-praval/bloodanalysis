import argparse
import logging
import pandas as pd
from app.services.ml_models import BloodAnalysisModel
from app.services.data_preprocessor import DataPreprocessor
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model():
    """Complete training pipeline using all 26 parameters"""
    parser = argparse.ArgumentParser(description='Train blood analysis model with 26 parameters')
    parser.add_argument('--dataset_path', type=str, required=True,
                       help='Path to the dataset directory containing PNG images')
    parser.add_argument('--labels_csv', type=str, default=None,
                       help='Path to CSV file with manual labels (optional)')
    parser.add_argument('--model_save_path', type=str, default='ml_models/blood_analysis_model.pkl',
                       help='Path to save the trained model')
    parser.add_argument('--extract_features_only', action='store_true',
                       help='Only extract features without training')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.dataset_path):
        logger.error(f"Dataset path {args.dataset_path} does not exist")
        return
    
    # Step 1: Extract features from all images
    logger.info("Step 1: Extracting features from all images...")
    preprocessor = DataPreprocessor()
    features_df = preprocessor.process_dataset(args.dataset_path, 'extracted_features.csv')
    
    if args.extract_features_only:
        logger.info("Feature extraction completed. Use --no-extract_features_only to train model.")
        return
    
    # Step 2: Train model
    logger.info("Step 2: Training model with all 26 parameters...")
    model = BloodAnalysisModel()
    
    try:
        model.train(
            dataset_path=args.dataset_path,
            labels_csv=args.labels_csv,
            test_size=0.2
        )
        
        # Save the trained model
        model.save_model(args.model_save_path)
        logger.info(f"Model successfully trained and saved to {args.model_save_path}")
        
        # Print feature importance
        if hasattr(model.models['rf'], 'feature_importances_'):
            feature_names = [
                'WBC', 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'PLT',
                'RDW_SD', 'RDW_CV', 'PDW', 'MPV', 'P_LCR', 'PCT', 'NEUT',
                'LYMPH', 'MONO', 'EO', 'BASO', 'IG', 'NRBCS', 'RETICULOCYTES',
                'IRF', 'LFR', 'MFR', 'HFR'
            ]
            importances = model.models['rf'].feature_importances_
            feature_imp_df = pd.DataFrame({
                'feature': feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
            
            logger.info("\nTop 10 Most Important Features:")
            for _, row in feature_imp_df.head(10).iterrows():
                logger.info(f"  {row['feature']}: {row['importance']:.3f}")
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    train_model()