from . import views
from django.urls import include,path

urlpatterns = [
    path('',views.index,name="expenses"),
    path('add-expense',views.add_expense,name="add-expenses")
]
