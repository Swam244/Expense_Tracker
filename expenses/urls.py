from . import views
from django.urls import include,path
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('',views.index,name="expenses"),
    path('add-expense',views.add_expense,name="add-expenses"),
    path('expense-edit/<int:id>',views.expense_edit,name="expense-edit"),
    path('expense-delete/<int:id>',views.expense_delete,name="expense-delete"),
    path('search-expenses',csrf_exempt(views.search_expense),name="search_expenses"),
    path('expense_category_summary',csrf_exempt(views.expense_category_summary),name="expense_category_summary"),
    path('expenseStats',views.stats_view,name="expenseStats"),
    path('export-csv',views.export_csv,name="export-csv"),
    path('export-excel',views.export_excel,name="export-excel"),
    path('export-pdf',views.html2pdf,name="export-pdf"),
]
