from django.urls import path, include
from . import views
from django.contrib import admin

admin.site.site_header = 'Restaurant Ordering'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('customer_signup', views.customer_signup, name='customer_signup'),
    path('customer_login', views.customer_login, name='customer_login'),
    path('customer_home/<int:pk>', views.customer_home, name='customer_home'),
    path('manager_signup', views.manager_signup, name='manager_signup'),
    path('manager_home/<int:pk>', views.manager_home, name='manager_home'),
    path('manager_login', views.manager_login, name='manager_login'),
    path('register_restaurant/<int:pk>', views.register_restaurant, name='register_restaurant'),
    path('reg_restaurant_home/<int:pk>', views.reg_restaurant_home, name='reg_restaurant_home'),
    path('add_item/<int:pk>', views.add_item, name='add_item'),    
]