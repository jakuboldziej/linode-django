from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name="index"),
    path('slider/', views.slider, name="slider"),
    path('smsapi/', views.smsapi, name="smsapi"),
    path('polls/', views.polls, name="polls"),
    path('createpoll/', views.createpoll, name="createpoll"),
    path('results/<int:poll_id>', views.results, name="results"),
    path('poll/<int:poll_id>', views.poll, name="poll"),
    # Events
    path('sendsms/', views.sendsms, name="sendsms"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.STATICFILES_STORAGE, document_root=settings.STATICFILES_STORAGE)
