from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.index, name='home'),
    path('dash', views.dash, name='dash'),
    path('dash/delete/<int:link_id>/', views.delete_url, name='delete_url'),
    path('dash/edit/<int:link_id>/', views.edit_url, name='edit_url'),
    path('<str:short_code>/', views.redirect_to_original, name='redirect_original'),
]