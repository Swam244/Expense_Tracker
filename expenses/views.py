from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import json


@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    currency = UserPreferences.objects.get(user = request.user).currency
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request,"expenses/index.html",{'categories':categories,'expenses':expenses,'page_obj':page_object,'currency':currency})

@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def add_expense(request):
    categories = Category.objects.all()
    values = request.POST
    if request.method == "GET":
        return render(request,"expenses/add-expense.html",{'categories':categories,'values':values})
    
    if request.method == "POST":
        
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required !!")
            return render(request,"expenses/add-expense.html",{'categories':categories,'values':values})
        
        description = request.POST['description']
        if not description:
            messages.error(request,"Description is required !!")
            return render(request,"expenses/add-expense.html",{'categories':categories,'values':values})
        
        category = request.POST['category']
        
        date = request.POST['expense_date']
        parsed_date = parse_date(date)
        if parsed_date:
            Expense.objects.create(owner=request.user,amount=amount,description=description,category=category,date=date)
            messages.success(request,"Expense Saved Successfully!!")
            return redirect('expenses')
        else:
            messages.error(request,"Please Specifiy Date of Expense")
            return render(request,"expenses/add-expense.html",{'categories':categories,'values':values})
    
@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def expense_edit(request,id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories,
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

        