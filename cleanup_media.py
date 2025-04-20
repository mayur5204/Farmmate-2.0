#!/usr/bin/env python
"""
Script to clean up old media files that are no longer referenced in the database.
This script is meant to be run as a cron job on Render.com.
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Set up Django environment
sys.path.append('model-project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model.settings')
django.setup()

from django.conf import settings
from community.models import Post
from users.models import UserProfile
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

def cleanup_community_posts():
    """Remove community post images older than 90 days that are no longer referenced in the database"""
    logger.info("Starting community post cleanup")
    
    # Get all media files from community posts in the database
    db_files = set()
    for post in Post.objects.all():
        if post.image:
            db_files.add(post.image.path)
    
    # Get all files in the media/community_posts directory
    media_dir = os.path.join(settings.MEDIA_ROOT, 'community_posts')
    if not os.path.exists(media_dir):
        logger.info(f"Directory {media_dir} does not exist, nothing to clean up")
        return
        
    # Check each file in the media directory
    count = 0
    for root, _, files in os.walk(media_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # If file is not in database and is older than 90 days, delete it
            if file_path not in db_files:
                file_stat = os.stat(file_path)
                file_time = datetime.fromtimestamp(file_stat.st_mtime)
                if datetime.now() - file_time > timedelta(days=90):
                    try:
                        os.remove(file_path)
                        count += 1
                        logger.info(f"Removed orphaned file: {file_path}")
                    except Exception as e:
                        logger.error(f"Error deleting {file_path}: {str(e)}")
    
    logger.info(f"Completed community post cleanup. Removed {count} orphaned files")

if __name__ == "__main__":
    logger.info("Starting media cleanup script")
    cleanup_community_posts()
    # Add more cleanup functions here as needed
    logger.info("Media cleanup complete")
