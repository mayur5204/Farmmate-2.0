#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to the Django project directory
cd model-project

# Create necessary media directories if they don't exist
mkdir -p media/community_posts/2025
mkdir -p media/profile_pics

# Copy default profile picture if it doesn't exist
if [ ! -f media/profile_pics/default.png ]; then
  cp -n static/images/farmerLogo.png media/profile_pics/default.png 2>/dev/null || :
fi

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate