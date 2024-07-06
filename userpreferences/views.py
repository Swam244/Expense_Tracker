from django.shortcuts import render
from django.views import View
import os
import json
from .models import UserPreferences
import pdb
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