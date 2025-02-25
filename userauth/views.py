from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, render
from userauth.forms import UserRegisterForm
from userauth.models import User

def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey {username}, Your account was created successfully!!!")
            new_user = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request,new_user)
            return redirect("core:index")
        else:
            print("wrong")
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request,'userauth/sign-up.html',context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,"Hey, you are already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            print(user)
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,"You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request,"User does not exists. create an account.")
        except:
            messages.warning(request,f"User with {email} does not exists")

    return render(request,'userauth/sign-in.html')

def logout_view(request):
    logout(request)
    messages.success(request,"You Logged out.")
    return redirect("userauth:sign-in")