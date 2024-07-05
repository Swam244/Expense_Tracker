from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse,HttpResponse
import json
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .utils import token_generator

class UsernameValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']
        print(username)
        if not str(username).isalnum():
            return JsonResponse({'username_error':"username should only contain alphanumeric characters."})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':"Username already in use"},status=409)
        
        return JsonResponse({'username_valid':"True"})

class EmailValidationView(View):
    def post(self,request):
        data = json.loads(request.body)
        email = data['email']
        print(email)
        if not validate_email(email):
            return JsonResponse({'email_error':"Email is invalid."})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':"email already in use"},status=409)
        
        return JsonResponse({'email_valid':"True"})

class RegistrationView(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    
    def post(self,request):
        loadPrevValues = {
            'values':request.POST
        }
        
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if password1!=password2:
                    messages.error(request,"Both Passwords Do not Match !!")
                    return render(request,'authentication/register.html',loadPrevValues)
                
                if len(password1) < 5:
                    messages.error(request,"Password length should be at least 5!!")
                    return render(request,'authentication/register.html', loadPrevValues)
                
                newUser = User.objects.create_user(username=username,email=email)
                newUser.set_password(password1)
                newUser.is_active = False
                
                #FOR GENERATING LINK 
                token = token_generator.make_token(newUser)
                domain = get_current_site(request).domain
                uidb64 = urlsafe_base64_encode(force_bytes(newUser.pk))
                print(uidb64)
                link = reverse('activate',kwargs={
                    'uidb64':uidb64,
                    'token':token
                })
                verificationLink = "http://"+domain+link
                email_subject = "Activate Your Account."
                email_body = "Hi "+newUser.username+" !!"+"\nPlease use this link to verify your Account\n"+verificationLink
                sendMail = EmailMessage(
                                    email_subject,
                                    email_body,
                                    "noreply@expenseTracker.com",
                                    [email],
                )
                sendMail.send(fail_silently=False)
                
                newUser.save()
                messages.success(request,"Account Created Successfully !!")
                return render(request,'authentication/register.html')
            
        return render(request,'authentication/register.html')

class VerificationView(View):
    def get(self,request,uidb64,token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not token_generator.check_token(user,token):
                return redirect('login'+'?message='+'User already Activated.')
            
            if user.is_active:
                return redirect('login')
            
            user.is_active = True
            user.save()
            messages.success(request,"Account Activated Successfully !!")
            return redirect('login')
        
        except Exception as err:
            pass
        
        return redirect('login')
    
class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = authenticate(username=username,password = password)
            if user:
                if user.is_active:
                    login(request,user)
                    messages.success(request,"Welcome " + username + ", \nYou're Now Logged In.")
                    return redirect('expenses')
                else:
                    messages.warning(request,"Your Account is Not Active.\nPlease check your email for verification link.")
                    return render(request,'authentication/login.html') 
            else:
                messages.error(request,"Invalid Credentials. Please try again.")
                return render(request,'authentication/login.html')
            
class LogoutView(View):
    def post(self,request):
        logout(request)
        messages.success(request,"You Have been Logged out !!")
        return redirect('login')