from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expense,newCat
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.http import JsonResponse,HttpResponse
from userpreferences.models import UserPreferences
from django.template.loader import render_to_string
from django.db.models import Sum
from .utils import html_to_pdf
import tempfile
import json
import datetime
import csv
import xlwt
import os

@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def index(request):
    cat = newCat.objects.all()
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    currency = UserPreferences.objects.filter(user = request.user).exists()
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    if currency:
        val = UserPreferences.objects.get(user=request.user).currency
        print(val)
    else:
        val = "INR - Indian Rupee"
    return render(request,"expenses/index.html",{'categories':categories,'expenses':expenses,'page_obj':page_object,'currency':val,'personalcat':cat})

@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def add_expense(request):
    cat = newCat.objects.all()
    categories = Category.objects.all()
    values = request.POST
    if request.method == "GET":
        return render(request,"expenses/add-expense.html",{'categories':categories,'values':values,'personalcat':cat})
    
    if request.method == "POST":
        
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required !!")
            return render(request,"expenses/add-expense.html",{'categories':categories,'values':values,'personalcat':cat})
        
        description = request.POST['description']
        if not description:
            messages.error(request,"Description is required !!")
            return render(request,"expenses/add-expense.html",{'categories':categories,'values':values,'personalcat':cat})
        
        category = request.POST['category']
        
        date = request.POST['expense_date']
        parsed_date = parse_date(date)
        if parsed_date:
            Expense.objects.create(owner=request.user,amount=amount,description=description,category=category,date=date)
            messages.success(request,"Expense Saved Successfully!!")
            return redirect('expenses')
        else:
            messages.error(request,"Please Specifiy Date of Expense")
            return render(request,"expenses/add-expense.html",{'categories':categories,'values':values,'personalcat':cat})
        
@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def expense_edit(request,id):
    cat = newCat.objects.all()
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories,
        'personalcat':cat,
    }
    if request.method == "GET":
        return render(request,'expenses/edit-expense.html',context)
    
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required !!")
            return render(request,"expenses/edit-expense.html",context)
     
        description = request.POST['description']
        if not description:
            messages.error(request,"Description is required !!")
            return render(request,"expenses/edit-expense.html",context)
        
        category = request.POST['category']
        
        date = request.POST['expense_date']
        parsed_date = parse_date(date)
        
        if parsed_date:
            expense.owner = request.user
            expense.amount = amount
            expense.category = category
            expense.description = description
            expense.date = date
            expense.save()
            messages.success(request,"Expense Updated Successfully!!")
            return redirect('expenses')
        
        else:
            messages.error(request,"Please Specifiy Date of Expense")
            return render(request,"expenses/edit-expense.html",context)
        
@login_required(login_url='authentication/login')   # Without login it cannot let the page reload. 
def expense_delete(request,id):
    expense = Expense.objects.get(pk = id)
    expense.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('expenses')

def search_expense(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get('searchText')
        expenses =  Expense.objects.filter(amount__istartswith = search_str , owner=request.user)|Expense.objects.filter(
                    date__istartswith = search_str,owner = request.user)|Expense.objects.filter(
                    description__icontains = search_str , owner=request.user)|Expense.objects.filter(
                    category__icontains = search_str , owner=request.user)
        
        data = expenses.values()
        return JsonResponse(list(data),safe=False)

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6) 
    expenses = Expense.objects.filter(owner=request.user, date__gte=six_months_ago, date__lte=todays_date)
    
    finalrep = {}
    
    def get_category(expense):
        return expense.category
    
    category_list = list(set(map(get_category, expenses)))
    
    def get_expense_category_amount(category):
        amount = 0
        filtered = expenses.filter(category=category)
        for item in filtered:
            amount += item.amount
        return amount
    
    for cat in category_list:
        finalrep[cat] = get_expense_category_amount(cat)
    print(finalrep)
    return JsonResponse({'expense_category_data': finalrep})


def stats_view(request):
    return render(request,'expenses/stats.html')

def export_csv(request):
    response = HttpResponse(content_type = "text/csv")
    response['Content-Disposition'] = 'attachment; filename=Expenses'+\
                                    str(datetime.datetime.now())+'.csv'
    print(response)
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])
    expenses = Expense.objects.filter(owner = request.user)
    
    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])
    
    return response

def export_excel(request):
    response = HttpResponse(content_type="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=Expenses'+\
                                    str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Amount','Description','Category','Date']
    for col_num in range(len(columns)):
        ws.write(row_num,col_num,columns[col_num],font_style)
    
    font_style = xlwt.XFStyle()
    
    rows = Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')
    
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num,col_num,str(row[col_num]),font_style)
            
    wb.save(response)
    return response

# def export_pdf(request):
#     os.add_dll_directory('C:\\Program Files\\GTK3-Runtime Win64\\bin')
#     response = HttpResponse(content_type="application/pdf")
#     response['Content-Disposition'] = 'attachment; filename=Expenses'+\
#                                     str(datetime.datetime.now())+'.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#     html_string = render_to_string('expenses/pdf-output.html',{'expenses':[],'total':0})
#     html = HTML(string=html_string)
#     result = html.write_pdf()
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name,'rb')
#         response.write(output.read())
    
#     return response
def html2pdf(request):
    values = Expense.objects.filter(owner=request.user)
    pdf = html_to_pdf("expenses/pdf-output.html",{"values":values})
    return HttpResponse(pdf,content_type="application/pdf")