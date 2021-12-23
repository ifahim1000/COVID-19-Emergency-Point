from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from .models import CustomUser, Buyer, Provider
from .forms import SignUpFormBuyer, SignUpFormPro

import random

def SignUser(request) :
    if request.method == 'POST' :
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        form = SignUpFormBuyer(request.POST, request.FILES)
        
        if CustomUser.objects.filter(email=email).exists() :
            messages.error(request, 'This email already exists, try another!')
            return redirect('/account/signup')
        else :
            user = CustomUser.objects.create_user(email=email, password=password, name=name, phone=phone, address=address)
            user.is_active=False
            user.save()
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            if form.is_valid() :
                if form.cleaned_data.get("image") :
                    photo = form.cleaned_data.get("image")
                    buyer = Buyer(user=user, image=photo, token=token)
                    buyer.save()
                else :
                    buyer = Buyer(user=user, token=token)
                    buyer.save()
            else :
                messages.error(request, 'Image upload error!')
                return redirect('/account/signup')
            
            #sending email
            current_site=get_current_site(request)
            mail_subject='Account Activation Link'
            message=render_to_string('activation.html',{
                'user':user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            email=EmailMessage(mail_subject,message, to=[email])
            email.send()
            messages.info(request,'Please check your email. We have sent an account activation link to activate your account.')
            
            # login(request, user) 
            return redirect('/account/login')
    else :
        form = SignUpFormBuyer()
    return render(request, 'login-signup.html', {'form' : form})

def SignProvider(request) :
    if request.method == 'POST' :
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']
        company_name = request.POST['company']
        form = SignUpFormPro(request.POST, request.FILES)
        lat = request.POST['lat']
        long = request.POST['long']
        if CustomUser.objects.filter(email=email).exists() :
            messages.error(request, 'This email already exists, try another!')
            return redirect('/account/sign-provider')
        else :
            user = CustomUser.objects.create_user(email=email, password=password, name=name, phone=phone, address=address)
            user.is_active=False
            user.save()
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            if form.is_valid() :
                if form.cleaned_data.get("image") :
                    photo = form.cleaned_data.get("image")
                    provider = Provider(user=user, company_name=company_name, image=photo, token=token, latitude=lat,longitude=long)
                    provider.save()
                else :
                    provider = Provider(user=user, company_name=company_name, token=token, latitude=lat,longitude=long)
                    provider.save()
            else :
                messages.error(request, 'Image upload error!')
                return redirect('/account/sign-provider')
            
            #sending email
            current_site=get_current_site(request)
            mail_subject='Account Activation Link'
            message=render_to_string('activation.html',{
                'user':user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            email=EmailMessage(mail_subject,message, to=[email])
            email.send()
            messages.info(request,'Please check your email. We have sent an account activation link to activate your account.')
            
            # login(request, user) 
            return redirect('/account/login')
    else :
        form = SignUpFormPro()
    return render(request, 'sign_provider.html', {'form' : form})

def LoginUser(request) :
    if request.method == 'POST' :
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None :
            login(request, user)
            return redirect('/')
        else :
            messages.error(request, 'Invalid email or password.')
    form=SignUpFormBuyer()
    return render(request, 'login-signup.html', {'form':form})

def LogoutUser(request) :
    if request.method == 'GET' :
        logout(request)
        messages.success(request, 'Logout successfully!')
        return redirect('/account/login')

def Activation(request, uidb64, token) :
    UserModel = get_user_model()
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError, CustomUser.DoesNotExist):
        user=None
    if user is not None :
        details = Buyer.objects.get(user=user)
        if details.token == token :
            user.is_active=True
            user.save()
            messages.success(request," Your account is activated. Now you can now log in")
            return redirect('/account/login')
        else :
            messages.warning(request, "Activation link is invalid")
            return redirect('/account/signup')
    else:
        messages.warning(request, "Activation link is invalid")
        return redirect('/account/signup')
    
def ForgotPass(request) :
    if request.method == 'POST' :
        email = request.POST['email']
        try :
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist :
            user = None
        if user is not None :
            code = random.randint(100000,999999)
            try :
                provider = Provider.objects.get(user=user)
            except Provider.DoesNotExist :
                provider = None
            try :
                buyer = Buyer.objects.get(user=user)
            except Buyer.DoesNotExist :
                buyer = None
            if provider is not None :
                provider.verification_code=code
                provider.save()
            elif buyer is not None :
                buyer.verification_code=code
                buyer.save()
            
            # sending email
            mail_subject='Verification Code'
            message=render_to_string('verification_code.html',{
                'user' : user,
                'code' : code,
            })
            email=EmailMessage(mail_subject,message, to=[email])
            email.send()
            
            messages.success(request, "Verification code has been sent to your email address.")
            return redirect('/account/reset-password/' + str(user.id))
        else :
            messages.error(request, "Email not found. Provide correct email address relative to your account")
            return redirect('/account/forgot-password')
    else :
        return render(request, 'forget_password.html')
    
def ResetPass(request, id) :
    if request.method == 'GET' :
        return render(request, 'reset_password.html', {'id':id})
    else :
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        code = request.POST['code']
        if pass1 == pass2 :
            user = CustomUser.objects.get(id=id)
            try :
                provider = Provider.objects.get(user=user)
            except Provider.DoesNotExist :
                provider = None
            try :
                buyer = Buyer.objects.get(user=user)
            except Buyer.DoesNotExist :
                buyer = None
            if buyer != None :
                if code == buyer.verification_code :
                    print(user.password)
                    user.set_password(pass1)
                    buyer.verification_code=None
                    buyer.save()
                    user.save()
                    messages.success(request, "Password changed successfully.")
                    return redirect('/account/login')
                else :
                    messages.error(request, "Verification code doesn't match.")
                    return redirect('/account/reset-password/'+id)
            else :
                if code == provider.verification_code :
                    user.set_password(pass1)
                    provider.verification_code=None
                    provider.save()
                    user.save()
                    messages.success(request, "Password changed successfully.")
                    return redirect('/account/login')
                else :
                    messages.error(request, "Verification code doesn't match.")
                    return redirect('/account/reset-password/'+id)
        else :
            messages.error(request, "Password doesn't match.")
            return redirect('/account/reset-password/'+id)

def Check(request) :
    if request.user.is_authenticated :
        try :
            buyer = Buyer.objects.get(user=request.user)
        except Buyer.DoesNotExist :
            buyer = None
            
        if buyer is None :
            return redirect('/profile/provider')
        else :
            return redirect('/profile/user')
    else :
        return redirect('/account/login')