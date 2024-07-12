from django.shortcuts import render
from expenses.models import Expense
from userincome.models import UserIncome
from userpreferences.models import UserPreferences
from django.contrib import messages
import datetime

def index(request):
    exist = UserPreferences.objects.filter(user = request.user).exists()
    if not exist:
        messages.info(request,"It is Recommended that you set your default currency. Please Check in General Settings")
        messages.info(request,"For now your default currency is INR - Indian Rupee")
        
    expenses = Expense.objects.filter(owner=request.user)
    income = UserIncome.objects.filter(owner=request.user)
    yearlyIncome = 0
    yearlyExpense = 0
    totalExpense = 0
    totalIncome = 0
    for i in expenses:
        totalExpense += float(i.amount)
    for i in income:
        totalIncome += float(i.amount)    

    currYear = datetime.datetime.now().year
    yearExpense = Expense.objects.filter(owner = request.user ,date__icontains=currYear)
    for yr in yearExpense:
        yearlyExpense += float(yr.amount)

    yearIncome = UserIncome.objects.filter(owner = request.user ,date__icontains=currYear)
    for yr in yearIncome:
        yearlyIncome += float(yr.amount)
        
    context = {'totalExpenses':totalExpense,
               'totalIncome':totalIncome,
               'expenseCnt':len(expenses),
               'incomeCnt':len(income),
               'yexpenseCnt':len(yearExpense),
               'yincomeCnt':len(yearIncome),
               'yearlyIncome':yearlyIncome,
               'yearlyExpense':yearlyExpense}
    
    return render(request,"index.html",context)
