from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from accounts.forms import SignUpForm, LoginForm
from orders.models import Profile


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "signup.html", {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                if request.user.is_superuser:
                    return redirect('/dashb')
                return redirect("/")

            else:
                msg = "Username or Password Doesn't match"

        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})
