from django.contrib import admin
from django.urls import path,include

admin.site.site_header = "Shorten.ly Administration"
admin.site.site_title = "Shorten.ly Admin Panel"
admin.site.index_title = "Welcome to Shorten.ly Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include ('home.urls'))
]

