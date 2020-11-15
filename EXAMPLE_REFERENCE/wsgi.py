import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EXAMPLE_REFERENCE.settings')

application = get_wsgi_application()