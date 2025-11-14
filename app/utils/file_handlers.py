import os
import shutil
import uuid
from typing import Optional
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
        logger.info(f"File handler initialized with upload folder: {upload_folder}")
    
    async def save_upload_file(self, file: UploadFile) -> str:
        """Save uploaded file and return file path"""
        try:
            # Generate unique filename
            file_extension = os.path.splitext(file.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(self.upload_folder, unique_filename)
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved successfully: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise
    
    def cleanup_file(self, file_path: str):
        """Remove temporary file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File cleaned up: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up file: {e}")
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from filename"""
        extension = os.path.splitext(filename)[1].lower().lstrip('.')
        if extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
            return 'image'
        elif extension == 'pdf':
            return 'pdf'
        elif extension == 'txt':
            return 'text'
        else:
            return 'unknown'
    
    def validate_file_type(self, filename: str) -> bool:
        """Validate if file type is supported"""
        file_type = self.get_file_type(filename)
        return file_type in ['image', 'pdf']