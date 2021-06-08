from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.
from orders.models import Course


def index(request):
    # portfolio_list = Course.objects.all().order_by('-created_on')
    # context = {
    #     "portfolio": portfolio_list,
    # }
    return render(request, "index.html")


def dashboard(request):
    return render(request, "dashboard/index.html")


# @login_required
# def dashboard(request):
#     return render(request, "dashboard/dashboard.html")
