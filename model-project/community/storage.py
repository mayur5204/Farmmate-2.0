from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import io
from PIL import Image
import logging
import traceback

logger = logging.getLogger(__name__)

class MobileCompatibleStorage(FileSystemStorage):
    """
    Custom storage backend that handles mobile image formats and converts them to compatible formats if needed
    """
    
    def _save(self, name, content):
        """Override the _save method to process images if needed"""
        # Check if this is an image file
        if self._is_image_file(name):
            # Try to handle HEIC/HEIF formats
            try:
                # Check if the file is a HEIC/HEIF format (commonly used in iOS)
                if name.lower().endswith(('.heic', '.heif')):
                    try:
                        # Import only when needed to avoid dependency issues
                        from pillow_heif import register_heif_opener
                        register_heif_opener()
                    except ImportError:
                        logger.warning("pillow_heif not installed. Cannot process HEIC/HEIF files.")
                        
                    # Convert the HEIC/HEIF to JPEG
                    img = Image.open(content)
                    buffer = io.BytesIO()
                    img = img.convert("RGB")  # HEIC can have alpha channel
                    img.save(buffer, format="JPEG", quality=90)
                    buffer.seek(0)
                    
                    # Change the file extension to jpg
                    name = os.path.splitext(name)[0] + '.jpg'
                    content = buffer
                    
                    logger.info(f"Converted HEIC/HEIF image to JPEG: {name}")
                
                # Process other image files as well to ensure consistency
                else:
                    # Read the image 
                    img = Image.open(content)
                    
                    # Resize if too large (optional)
                    max_size = 1920  # Max dimension
                    if max(img.size) > max_size:
                        img.thumbnail((max_size, max_size), Image.LANCZOS)
                    
                    # Create a new buffer for the processed image
                    buffer = io.BytesIO()
                    
                    # Save with appropriate format and compression
                    if name.lower().endswith(('.jpg', '.jpeg')):
                        img = img.convert("RGB")
                        img.save(buffer, format="JPEG", quality=85)
                    elif name.lower().endswith('.png'):
                        img.save(buffer, format="PNG", optimize=True)
                    elif name.lower().endswith('.gif'):
                        img.save(buffer, format="GIF")
                    else:
                        # For unknown formats, convert to JPEG
                        img = img.convert("RGB")
                        img.save(buffer, format="JPEG", quality=85)
                        name = os.path.splitext(name)[0] + '.jpg'
                    
                    buffer.seek(0)
                    content = buffer
                    
                    logger.info(f"Processed image: {name}")
                    
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                logger.error(traceback.format_exc())
                # Continue with the original file if processing fails
        
        # Let the parent class save the file
        return super()._save(name, content)
    
    def _is_image_file(self, name):
        """Check if the file is an image based on extension"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.heic', '.heif']
        return any(name.lower().endswith(ext) for ext in image_extensions)