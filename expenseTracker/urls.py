from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expenses/',include('expenses.urls')),
    path('',include('authentication.urls')),
    path('preferences/',include('userpreferences.urls')),
    path('income/',include('userincome.urls')),
    path('dashboard/',include('dashboard.urls')),
    path('acsettings/',include('acsettings.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)