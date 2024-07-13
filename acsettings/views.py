from django.shortcuts import render,redirect
from userincome.models import newSrc
from expenses.models import newCat
from django.core.paginator import Paginator

def index(request):
    existsExpenseCat = newCat.objects.filter(owner = request.user).exists()
    existsIncomeSrc = newSrc.objects.filter(owner = request.user).exists()
    
    if existsExpenseCat == False and existsIncomeSrc == False:
        return render(request,"acsettings/index.html")
    
    expenseCat = newCat.objects.filter(owner = request.user)
    if existsIncomeSrc == False:
        return render(request,"acsettings/index.html",{'expenseCat':expenseCat})
    
    incomeSrc = newSrc.objects.filter(owner = request.user)
    if existsExpenseCat == False:
        return render(request,"acsettings/index.html",{'incomeSrc':incomeSrc})
    
    else:
        return render(request,"acsettings/index.html",{'expenseCat':expenseCat,'incomeSrc':incomeSrc})