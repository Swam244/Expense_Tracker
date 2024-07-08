from django.shortcuts import render,redirect
from django.views import View
import os
from .models import UserPreferences
from expenses.models import newCat
from userincome.models import newSrc
import pdb
import json
from django.contrib import messages
from django.conf import settings


class Index(View):         
    def get(self, request):
        currencyData = []
        preferenceExists = UserPreferences.objects.filter(user=request.user).exists()
        user_preferences = None
        if preferenceExists:
            user_preferences = UserPreferences.objects.get(user=request.user)
        
        filePath = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(filePath, 'r') as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                currencyData.append({'name': key,
                                 'value': value})
        return render(request, 'preferences/index.html', {'currencies': currencyData,'preferences':user_preferences})

    def post(self,request):
        currencyData = []
        filePath = os.path.join(settings.BASE_DIR, 'currencies.json')
        with open(filePath, 'r') as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                currencyData.append({'name': key,
                                 'value': value})
                
        newCurrency = request.POST['currency']
        preferenceExists = UserPreferences.objects.filter(user=request.user).exists()
        user_preferences = None
        if preferenceExists:
            user_preferences = UserPreferences.objects.get(user=request.user)
            user_preferences.currency = newCurrency
            user_preferences.save()
        else:
            UserPreferences.objects.create(user=request.user,currency=newCurrency)
        messages.success(request,"Changes Saved")
        user_preferences = UserPreferences.objects.get(user=request.user)
        return render(request,'preferences/index.html',{'currencies':currencyData,'preferences':user_preferences})
    
def add_income_src(request):
    if request.method == "POST":
        src = request.POST['source']
        print(src)
        if not src:
            messages.error(request,"Please Provide a Valid Response")
            return redirect('preferences')
        exists = newSrc.objects.filter(owner=request.user,name = str(src).upper()).exists()
        if exists:
            messages.error(request,"Category Already Exists!")
            return redirect('preferences')
        newSrc.objects.create(owner = request.user,name = str(src).upper())    
        messages.success(request,"New Income Source Added Successfully !!")
        return redirect('preferences') 

def add_expense_cat(request):
   if request.method == "POST":
        cat = request.POST['cat']
        if not cat:
            messages.error(request,"Please Provide a Valid Response")
            return redirect('preferences')
        exists = newCat.objects.filter(owner=request.user,name = str(cat).upper()).exists()
        if exists:
            messages.error(request,"Category Already Exists!")
            return redirect('preferences')
        newCat.objects.create(owner=request.user,name = str(cat).upper())
        messages.success(request,"New Expense Category Added Successfully !!")
        return redirect('preferences')