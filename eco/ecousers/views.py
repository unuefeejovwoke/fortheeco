from email.policy import default
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import RegistrationForm
#email verify
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
           
            
            #user activation
            current_site = get_current_site(request)
            mail_subject = "WElcome to ECO, Please activate your account"
            message = render_to_string('ecousers/account_verification_email.html', {
                'user': user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, "Account created successfully")
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'ecousers/register.html', context)

#this method to allow user login by email and i will call it in login view
def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except:
        return None

def login(request):
    if request.method =='POST':
        email = request.POST['email']
        password = request.POST['password']
        username = get_user(email)

        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            if 'remember_me' in request.POST:
                request.session.set_expiry(1209600) # 2 weeks

            messages.success(request,'you are now logged in')
            return redirect(request.GET['next'] if 'next' in request.GET else '/')
        else:
            messages.error(request,'invalid email or password')
            return redirect('ecousers:login')

    return render(request,'ecousers/login.html')

@login_required(login_url="ecousers:login")
def logout(request):
    auth.logout(request)
    messages.success(request, "You are now logged out")
    return redirect('ecousers:login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations!! Your account is activated')
        return redirect('ecousers:login')
        
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('ecousers:register')