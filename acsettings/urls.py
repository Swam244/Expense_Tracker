from django.contrib import admin
from django.urls import path,include
from .views import index, change_password

urlpatterns = [
    path('',index,name="acsettings"),    
    path('change-password',change_password,name='change-password'),
]
