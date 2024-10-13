
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', include('Orders.urls')),
    path('products/', include('products.urls')),
]
