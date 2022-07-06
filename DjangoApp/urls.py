from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
]
admin.AdminSite.site_title = "Website Administration"
admin.AdminSite.site_header = "Website Administration"
admin.AdminSite.index_title = "Website Administration"
handler404 = 'website.views.view_page_not_found'
