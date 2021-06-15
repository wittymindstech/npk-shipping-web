from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from orders.models import Profile
from django.contrib.auth.models import User 
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


def register(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "Username is taken")
                return render(request, "auth/sign-up.html",)
            if User.objects.filter(email__iexact=email).exists():
                messages.error(request, "Email id already in use.")
                return render(request, "auth/sign-up.html",)
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            Profile.objects.create(user=user)
            messages.success(request, "Sign Up Successfull! ")
            return redirect('login')
        elif request.method == "GET":
            return render(request, "auth/sign-up.html",)
        else:
            return render(request, "auth/sign-up.html",)
    except:            
        messages.error(request, "Something went wrong. Please try again.")
        return render(request, "auth/sign-up.html",)


def login_view(request):
    # form = LoginForm(request.POST or None)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password, end="\n\n", sep=" | ")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                messages.success(request, "Sign in Successful.")
                return redirect('/dashboard')
            messages.success(request, "Sign in Successful.")
            return redirect("/")

        else:
            messages.error(request, "Username or Password Doesn't match")
            return render(request, "auth/login.html",)
    elif request.method == "GET":
        return render(request, "auth/login.html",)
    else:
        messages.error(request, "Error validating the form")
        return render(request, "auth/login.html",)
