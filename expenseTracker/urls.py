from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/',include('expenses.urls')),
    path('',include('authentication.urls')),
    path('preferences/',include('userpreferences.urls')),
    path('income/',include('userincome.urls')),
    path('dashboard/',include('dashboard.urls')),
]
