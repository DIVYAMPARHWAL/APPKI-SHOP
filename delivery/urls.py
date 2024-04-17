
app_name = 'delivery'
from django.contrib import admin
from django.urls import path,include
from .views import DeliveryView

urlpatterns = [
    path('', DeliveryView, name='delV'),
]