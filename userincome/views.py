from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Source,UserIncome,newSrc
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreferences
from django.http import HttpResponse
import datetime
import csv
import json
import xlwt

@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def index(request):
    personalSources = newSrc.objects.all()
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    currency = UserPreferences.objects.filter(user = request.user).exists()
    paginator = Paginator(income,5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    if currency:
        val = UserPreferences.objects.get(user=request.user).currency
        print(val)
    else:
        val = "INR - Indian Rupee"
    return render(request,"income/index.html",{'sources':sources,'income':income,'page_obj':page_object,'currency':val,'personalsrc':personalSources})


@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def add_income(request):
    sources = Source.objects.all()
    personalSources = newSrc.objects.all()
    values = request.POST
    if request.method == "GET":
        return render(request,"income/add-income.html",{'sources':sources,'values':values,'personalsrc':personalSources})
    
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required !!")
            return render(request,"income/add-income.html",{'sources':sources,'values':values,'personalsrc':personalSources})
        if float(amount) == 0.0:
            messages.error(request,"Amount cannot be Zero !!")
            return render(request,"income/add-income.html",{'sources':sources,'values':values,'personalsrc':personalSources})
        description = request.POST['description']
        if not description:
            messages.error(request,"Description is required !!")
            return render(request,"expenses/add-expense.html",{'sources':sources,'values':values,'personalsrc':personalSources})
        
        source = request.POST['source']
        print(source)
        
        date = request.POST['income_date']
        parsed_date = parse_date(date)
        if parsed_date:
            UserIncome.objects.create(owner=request.user,amount=amount,description=description,source=source,date=date)
            messages.success(request,"Income Saved Successfully!!")
            return redirect('income')
        else:
            messages.error(request,"Please Specifiy Date of Income")
            return render(request,"income/add-income.html",{'sources':sources,'values':values,'personalsrc':personalSources})
    
@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def income_edit(request,id):
    sources = Source.objects.all()
    personalSources = newSrc.objects.all()
    income = UserIncome.objects.get(pk=id)
    context = {
        'income':income,
        'values':income,
        'sources':sources,
        'personalsrc':personalSources
    }
    if request.method == "GET":
        return render(request,'income/edit-income.html',context)
    
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required !!")
            return render(request,"income/edit-income.html",context)
     
        description = request.POST['description']
        if not description:
            messages.error(request,"Description is required !!")
            return render(request,"income/edit-income.html",context)
        
        source = request.POST['source']
        
        date = request.POST['income_date']
        parsed_date = parse_date(date)
        
        if parsed_date:
            income.owner = request.user
            income.amount = amount
            income.source = source
            income.description = description
            income.date = date
            income.save()
            messages.success(request,"Income Updated Successfully!!")
            return redirect('income')
        
        else:
            messages.error(request,"Please Specifiy Date of Income")
            return render(request,"income/edit-income.html",context)
        
@login_required(login_url='authentication/login')   # Without login it cannot let the page reload. 
def income_delete(request,id):
    income = UserIncome.objects.get(pk = id)
    income.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('income')

def search_income(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        income =  UserIncome.objects.filter(amount__istartswith = search_str , owner=request.user)|UserIncome.objects.filter(
                    date__istartswith = search_str,owner = request.user)|UserIncome.objects.filter(
                    description__icontains = search_str , owner=request.user)|UserIncome.objects.filter(
                    source__icontains = search_str , owner=request.user)
        
        data = income.values()
        return JsonResponse(list(data),safe=False)
    
def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6) 
    income = UserIncome.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    
    finalrep = {}
    
    def get_source(income):
        return income.source
    
    source_list = list(set(map(get_source, income)))
    
    def get_income_source_amount(source):
        amount = 0
        filtered = UserIncome.objects.filter(source=source)
        for item in filtered:
            amount += item.amount
        return amount
    
    for src in source_list:
        finalrep[src] = get_income_source_amount(src)
    print(finalrep)
    return JsonResponse({'income_source_data': finalrep})

def stats_view(request):
    return render(request,'income/stats.html')

    
def export_csv(request):
    response = HttpResponse(content_type = "text/csv")
    response['Content-Disposition'] = 'attachment; filename=Income'+\
                                    str(datetime.datetime.now())+'.csv'
    print(response)
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Source','Date'])
    income = UserIncome.objects.filter(owner = request.user)
    
    for i in income:
        writer.writerow([i.amount,i.description,i.source,i.date])
    
    return response

def export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=Income'+\
                                    str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount','Description','Source','Date']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    
    font_style = xlwt.XFStyle()
    
    rows = UserIncome.objects.filter(owner=request.user).values_list('amount','description','source','date')
    
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
            
    wb.save(response)
    return response