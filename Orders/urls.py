from django.contrib import admin
from django.urls import path,include
from . import views



urlpatterns = [
    path('', views.create_order, name='create_order'),
    path('customers',views.get_all_customers,name='customers'),
    path('products',views.get_all_products,name='customer'),
]
