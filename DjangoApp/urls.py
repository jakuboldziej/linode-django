from django.contrib import admin
from django.urls import path, include
from website import views as wviews

urlpatterns = [
    path('', include('website.urls')),
    # Auth
    path('admin/', admin.site.urls),
    path('', include("django.contrib.auth.urls")),
    path('register/', wviews.register, name="register"),
] 
admin.AdminSite.site_title = "Website Administration"
admin.AdminSite.site_header = "Website Administration"
admin.AdminSite.index_title = "Website Administration"
handler404 = 'website.views.view_page_not_found'
