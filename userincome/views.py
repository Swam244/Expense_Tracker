from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Source,UserIncome
from django.contrib import messages
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.http import JsonResponse
from userpreferences.models import UserPreferences
import json

@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    currency = UserPreferences.objects.get(user = request.user).currency
    paginator = Paginator(income,5)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request,"income/index.html",{'sources':sources,'income':income,'page_obj':page_object,'currency':currency})


@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def add_income(request):
    sources = Source.objects.all()
    values = request.POST
    if request.method == "GET":
        return render(request,"income/add-income.html",{'sources':sources,'values':values})
    
    if request.method == "POST":
        amount = request.POST['amount']
        if not amount:
            messages.error(request,"Amount is required !!")
            return render(request,"income/add-income.html",{'sources':sources,'values':values})
        
        description = request.POST['description']
        if not description:
            messages.error(request,"Description is required !!")
            return render(request,"expenses/add-expense.html",{'sources':sources,'values':values})
        
        source = request.POST['source']
        
        date = request.POST['income_date']
        parsed_date = parse_date(date)
        if parsed_date:
            UserIncome.objects.create(owner=request.user,amount=amount,description=description,source=source,date=date)
            messages.success(request,"Income Saved Successfully!!")
            return redirect('income')
        else:
            messages.error(request,"Please Specifiy Date of Income")
            return render(request,"income/add-income.html",{'sources':sources,'values':values})
    
@login_required(login_url='authentication/login')   # Without login it cannot let the page reload.
def income_edit(request,id):
    sources = Source.objects.all()
    income = UserIncome.objects.get(pk=id)
    context = {
        'income':income,
        'values':income,
        'sources':sources,
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