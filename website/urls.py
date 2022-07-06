from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('slider/', views.slider, name="slider"),
] + static(settings.STATICFILES_STORAGE, document_root=settings.STATICFILES_STORAGE)
