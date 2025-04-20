import os
import datetime
import shutil

def clean_old_media(media_dir, days_old=30):
    """
    Remove media files older than the specified number of days
    """
    today = datetime.datetime.now()
    cutoff = today - datetime.timedelta(days=days_old)
    
    print(f"Cleaning files older than {days_old} days...")
    removed_count = 0
    
    # Walk through all directories in the media folder
    for root, dirs, files in os.walk(media_dir):
        # Skip the default profile pic
        if "default.png" in files and "profile_pics" in root:
            files.remove("default.png")
            
        for file in files:
            file_path = os.path.join(root, file)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            
            if file_modified < cutoff:
                try:
                    os.remove(file_path)
                    print(f"Removed: {file_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"Error removing {file_path}: {e}")
    
    # Clean empty directories
    for root, dirs, files in os.walk(media_dir, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):  # Check if directory is empty
                try:
                    os.rmdir(dir_path)
                    print(f"Removed empty directory: {dir_path}")
                except Exception as e:
                    print(f"Error removing directory {dir_path}: {e}")
    
    print(f"Cleanup complete. Removed {removed_count} files.")

if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    # Get the directory of the script
    script_dir = Path(__file__).resolve().parent
    # Media directory path
    media_dir = script_dir / "model-project" / "media"
    
    # Default to 30 days if no argument is provided
    days = 30
    if len(sys.argv) > 1:
        try:
            days = int(sys.argv[1])
        except ValueError:
            print(f"Invalid days value: {sys.argv[1]}. Using default of 30 days.")
    
    clean_old_media(media_dir, days)
