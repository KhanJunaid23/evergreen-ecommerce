from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from userauth.forms import UserRegisterForm

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