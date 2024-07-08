from . import views
from django.urls import include,path
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    path('',views.index,name='income'),
    path('add-income',views.add_income,name="add-income"),
    path('income-edit/<int:id>',views.income_edit,name="income-edit"),
    path('income-delete/<int:id>',views.income_delete,name="income-delete"),
    path('search-income',csrf_exempt(views.search_income),name="search-income"),
    path('export-csv',views.export_csv,name="export-csv"),
    path('export-excel',views.export_excel,name="export-excel"),
    path('income_source_summary',csrf_exempt(views.income_source_summary),name="income_source_summary"),
    path('incomeStats',views.stats_view,name="incomeStats"),
]
