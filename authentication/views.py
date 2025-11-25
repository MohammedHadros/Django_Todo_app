from django.shortcuts import render,redirect
from django.contrib import messages
from validate_email import validate_email
from .models import User
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from helpers.decorators import auth_user_should_not_access
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.contrib.messages import get_messages
# Create your views here.


class EmailTread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)
    def run(self):
        if not settings.TESTING:
            self.email.send()



def send_activation_email(user,request):
    current_site=get_current_site(request)
    email_subject='Activate your account'
    emai_body=render_to_string('authentication/activate.html',{
        'user':user,
        'domin':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user),
    })
    email=EmailMessage(subject=email_subject,
                       body=emai_body,
                       from_email= settings.EMAIL_FROM_USER,
                       to=[user.email])
    EmailTread(email).start()



@auth_user_should_not_access
def register(request):
    context={}
    if request.method=="POST":
        context={'has_error':False , 'data':request.POST}
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        conpassword=request.POST.get('conpassword')
        if len(password)<6:
            messages.add_message(request,messages.WARNING,
                    "Password is short , Password should be at least 6 Charecters")
            context['has_error']=True
        if password!=conpassword:
            messages.add_message(request,messages.WARNING,"Password Not Matched")
            context['has_error']=True
        if not validate_email(email):
            messages.add_message(request,messages.WARNING,"Email is not valid")
            context['has_error']=True
        if not username:
            messages.add_message(request,messages.WARNING,"username is required")
            context['has_error']=True
        if User.objects.filter(username=username).exists():
            messages.add_message(request,messages.WARNING,
                    "username is Tacken, Please enter another username")
            context['has_error']=True
            return render (request,"authentication/register.html" ,context , status=409)
            
        if User.objects.filter(email=email).exists():
            messages.add_message(request,messages.WARNING,
                    "Email is Tacken, Please enter another Email")
            context['has_error']=True
            return render (request,"authentication/register.html" ,context , status=419)


        if context['has_error']:
            return render (request,"authentication/register.html" ,context)
        user=User.objects.create_user(username=username , email=email)
        user.set_password(password)
        user.save()
        messages.add_message(request,messages.SUCCESS,"User has been created Sucsessfuly")
        send_activation_email(user,request)
        messages.add_message(request,messages.SUCCESS,"Verify your email account , Check your email box")
        return redirect('login')
    return render (request,"authentication/register.html",context)

@auth_user_should_not_access
def login_user(request):
    if request.method=='POST':
        context={ 'data':request.POST}
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if not user:
            messages.add_message(request,messages.ERROR,"invalid credentials")
            return render (request,"authentication/login.html" ,context)
        if not user.is_email_verified:
            messages.add_message(request,messages.ERROR,"Email is not verivied , Please check your email inbox")
            send_activation_email(user,request)
            return render (request,"authentication/login.html" ,context)
        login(request,user)
        messages.add_message(request,messages.SUCCESS,f"Welcome {user.username}")
        return redirect(reverse('Home'))
    return render (request,"authentication/login.html")


@login_required
def logout_user(request):
    logout(request)
    messages.add_message(request,messages.SUCCESS,'logged out sucsessfully')

    return redirect(reverse( 'login'))




def activate_user_email(request , uidb64 ,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except Exception as e:
        print(e)
        user=None

    if user and generate_token.check_token(user,token):
        user.is_email_verified=True
        user.save()

        messages.add_message(request,messages.SUCCESS,
                'Email has been verified sucssesfully, You can login now')
        return redirect(reverse('login'))
    
    return render(request,"authentication/activation_failed.html",{'user':user})