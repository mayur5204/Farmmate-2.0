"""
WSGI config for model project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Set path to the project directory - uncomment and modify when deploying to PythonAnywhere
# path = '/home/yourusername/Farmmate-2.0/model-project'
# if path not in sys.path:
#     sys.path.insert(0, path)

# Set environment variables for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model.settings')
os.environ['DJANGO_DEBUG'] = 'False'

# Use a secret key from environment variable in production
# Comment out the below line if setting the secret key in PythonAnywhere dashboard
# os.environ['DJANGO_SECRET_KEY'] = 'your-secure-key-here'

application = get_wsgi_application()
