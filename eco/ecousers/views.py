from email.policy import default
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse


from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from .models import Account, UserProfile
from .forms import RegistrationForm, UserForm, UserProfileForm

from ecoplatform.models import Problem, Project
#email verify
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings

import requests
def signup_redirect(request):
    messages.error(request, "You already have an account!")
    return redirect ("homepage")

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Welcome to the ECO Platform!. Please click the below link to activate your account'
            message = render_to_string('ecousers/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address  Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'ecousers/register.html', context)

def login(request):
    if request.method =="POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

            return redirect('ecousers:dashboard')

        else:
            messages.error(request, "Invalid login credentials")
            return redirect('ecousers:login')
    return render(request, 'ecousers/login.html')

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
        
        # USER Welcome mail
        
        current_site = get_current_site(request)
        mail_subject = 'Welcome to the ECO Platform!. Please click the below link to activate your account'
        message = render_to_string('ecousers/account_welcome_mail.html', {
            'user': user,
            'domain': current_site,
        
        })
        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        
        messages.success(request, 'Congratulations!! Your account is activated')
        return redirect('ecousers:login')
        
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('ecousers:register')
    
@login_required(login_url = 'ecousers:login')
def dashboard(request):
    projects = Project.objects.order_by('-created').filter(user_id=request.user.id)
    projects_count = projects.count()
    
    problems = Problem.objects.order_by('-created').filter(user_id=request.user.id)
    problems_count = problems.count()
    
    context = {
        'projects_count': projects_count,
        'problems_count':problems_count,
    
    }
    return render(request, 'ecousers/dashboard.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # forgot password mail
            #user activation
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('ecousers/reset_password_email.html', {
                'user': user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Password reset email has been sent to your mail')
            return redirect('ecousers:login')
        
        else:
            messages.error(request, 'Account does not exist')
            return redirect('ecousers:forgotPassword')
    return render(request,'ecousers/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user =None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('ecousers:resetPassword')
    else:
        messages.success(request, 'This link has expired')
        return redirect('ecousers:login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return render(request, 'ecousers/passwordConfirm.html')
        else:
            messages.error(request, "Password doesn't match")
            return redirect('ecousers:resetPassword')
    else:
        return render(request,'ecousers/resetPassword.html')
    
@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('ecousers:edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'ecousers/edit_profile.html', context)

@login_required(login_url='ecousers:login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('ecousers:change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('ecousers:change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('ecousers:change_password')
    return render(request, 'ecousers/change_password.html')