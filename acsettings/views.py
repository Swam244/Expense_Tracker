from django.shortcuts import render,redirect
from userincome.models import newSrc
from expenses.models import newCat
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages


def index(request):
    context = {}
    existsExpenseCat = newCat.objects.filter(owner = request.user).exists()
    existsIncomeSrc = newSrc.objects.filter(owner = request.user).exists()
    if existsExpenseCat:
        expenseCat = newCat.objects.filter(owner = request.user)
        context['expenseCat'] = expenseCat
    
    if existsIncomeSrc:
        incomeSrc = newSrc.objects.filter(owner = request.user)
        context['incomeSrc'] = incomeSrc
    return render(request,"acsettings/index.html",context)

    
def change_password(request):
    if request.method == "POST":
        oldPass = request.POST['oldpass']
        user = request.user
        oldPassCheck = check_password(oldPass,user.password)
        if oldPassCheck:
            return render(request,"acsettings/pass-change.html")
        else:
            messages.error(request,"Entered Password is Incorrect!")
            return render(request,"acsettings/pass-change.html")
    else:
        return render(request,"acsettings/pass-change.html")