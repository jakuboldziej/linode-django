import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

application = get_wsgi_application()

if settings.DEBUG:
    application = WhiteNoise(application, root="/path/to/static/files")
    application.add_files("/path/to/more/static/files", prefix="more-files/")