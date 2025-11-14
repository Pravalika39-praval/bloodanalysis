import pytesseract
from PIL import Image
import pdf2image
import logging
import os
from typing import Optional
import cv2
import numpy as np

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, tesseract_path: Optional[str] = None):
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            logger.info(f"Tesseract initialized with path: {tesseract_path}")
        else:
            logger.warning("Tesseract path not provided or invalid, using default")
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for better OCR results"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Apply noise removal
            denoised = cv2.medianBlur(gray, 3)
            
            # Apply thresholding
            _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            return thresh
        except Exception as e:
            logger.error(f"Image preprocessing error: {e}")
            return image
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image file"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Could not read image file: {image_path}")
            
            logger.info(f"Processing image: {image_path}")
            
            # Preprocess image
            processed_image = self.preprocess_image(image)
            
            # OCR configuration for medical reports
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;()-/ '
            
            # Extract text
            text = pytesseract.image_to_string(processed_image, config=custom_config)
            
            logger.info(f"Successfully extracted text from image: {image_path}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from image {image_path}: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            # Convert PDF to images
            images = pdf2image.convert_from_path(pdf_path)
            
            all_text = []
            for i, image in enumerate(images):
                # Convert PIL image to OpenCV format
                open_cv_image = np.array(image)
                open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR
                
                # Preprocess and extract text
                processed_image = self.preprocess_image(open_cv_image)
                text = pytesseract.image_to_string(processed_image)
                all_text.append(text)
                
                logger.info(f"Processed page {i+1} of PDF")
            
            combined_text = "\n".join(all_text)
            logger.info(f"Successfully extracted text from PDF: {pdf_path}")
            return combined_text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            return ""
    
    def extract_text_from_file(self, file_path: str, file_type: str) -> str:
        """Extract text from various file types"""
        try:
            if file_type.lower() in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
                return self.extract_text_from_image(file_path)
            elif file_type.lower() == 'pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_type.lower() == 'txt':
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read()
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return ""