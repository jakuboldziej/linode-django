from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
]

handler404 = 'website.views.view_page_not_found'
