from django.urls import path
from . import views
urlpatterns = [
    path('',views.Index.as_view(),name="preferences"),
    path('add-income-src',views.add_income_src,name='add_income_src'),
    path('add-expense-cat',views.add_expense_cat,name='add_expense_cat'),   
]
