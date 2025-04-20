"""
WSGI configuration file for PythonAnywhere.
This file should be used as a template for the WSGI configuration on PythonAnywhere.
"""

import os
import sys

# Add your project directory to the path
# Replace 'yourusername' with your PythonAnywhere username
path = '/home/yourusername/Farmmate-2.0/model-project'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'model.settings'
os.environ['DJANGO_DEBUG'] = 'False'
# Generate a secure secret key and set it here or in PythonAnywhere dashboard
os.environ['DJANGO_SECRET_KEY'] = 'your-secure-key-here'

# Import Django and start application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()