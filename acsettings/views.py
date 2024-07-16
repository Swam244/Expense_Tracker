from django.shortcuts import render,redirect
from userincome.models import newSrc
from expenses.models import newCat
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
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

@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        oldPass = request.POST['oldpass']
        user = request.user
        oldPassCheck = check_password(oldPass,user.password)
        context = {
            'oldpass':oldPass
        }
        if oldPassCheck:
            newPass1 = request.POST['newPassword']    
            newPass2 = request.POST['confirmPassword']

            if newPass2 != newPass1:
                messages.error(request,"Both passwords do not Match !!")
                context['newpass1'] = newPass1
                context['newpass2'] = newPass2
                return render(request,"acsettings/pass-change.html",context)
            
            else:
                if len(newPass1) < 5:
                    messages.error(request,"Password Length should be atleast 5 !!")
                    return render(request,"acsettings/pass-change.html",context)
                else:
                    messages.success(request,"Password Changed Succesfully !!")
                    messages.success(request,"Please login using new Password")
                    user.set_password(newPass1)
                    user.save()
                    return redirect('acsettings')
            
        else:
            messages.error(request,"Entered Password is Incorrect!")
            return render(request,"acsettings/pass-change.html",context)
    else:
        return render(request,"acsettings/pass-change.html")