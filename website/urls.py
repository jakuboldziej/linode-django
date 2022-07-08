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
    path('vote/<int:poll_id>', views.vote, name="vote"),
    # Events
    path('sendsms/', views.sendsms, name="sendsms"),
    path("logout/", views.logout, name="logout"),
    path("addimage/", views.addimage, name="addimage"),
    path("deleteimage/", views.deleteimage, name="deleteimage"),
    path("deletepoll/<int:poll_id>", views.deletepoll, name="deletepoll"),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.STATICFILES_STORAGE, document_root=settings.STATICFILES_STORAGE)
