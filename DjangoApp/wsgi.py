import os

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoApp.settings')

application = get_wsgi_application()

application = WhiteNoise(application, root="/var/www/DjangoApp/static")
application.add_files("/var/www/DjangoApp/static", prefix="more-files/")
