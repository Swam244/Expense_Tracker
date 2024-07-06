from . import views
from django.urls import include,path
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('',views.index,name="expenses"),
    path('add-expense',views.add_expense,name="add-expenses"),
    path('expense-edit/<int:id>',views.expense_edit,name="expense-edit"),
    path('expense-delete/<int:id>',views.expense_delete,name="expense-delete"),
    path('search-expenses',csrf_exempt(views.search_expense),name="search_expenses"),
]
