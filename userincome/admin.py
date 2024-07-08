from django.contrib import admin
from . models import UserIncome,Source,newSrc

class IncomeAdmin(admin.ModelAdmin):
    list_display = ['amount','description','owner','source','date',]
    search_fields = ('description','source','date')
admin.site.register(UserIncome,IncomeAdmin)
admin.site.register(Source)
admin.site.register(newSrc)
