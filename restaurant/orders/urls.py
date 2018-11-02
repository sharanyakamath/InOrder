from django.urls import path, include
from . import views
from django.contrib import admin

admin.site.site_header = 'Restaurant Ordering'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('customer_signup', views.customer_signup, name='customer_signup'),
    path('customer_login', views.customer_login, name='customer_login'),
    path('customer_home/<int:pk>', views.customer_home, name='customer_home'),
]