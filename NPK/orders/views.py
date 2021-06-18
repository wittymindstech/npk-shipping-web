from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from orders.models import Course, Order, OrderItem, Profile
from orders.forms import CheckoutForm


def index(request):
    portfolio_list = Course.objects.all().order_by('-created_on')
    context = {
        "portfolio": portfolio_list,
    }
    return render(request, "index.html", context)


def dashboard(request):
    return render(request, "dashboard/index.html")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            return render(self.request, 'ordersummary.html',
                          context={'object': order})
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any courses in cart")
            return redirect('/')

    model = Order
    template_name = 'ordersummary.html'


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form,
        }
        return render(self.request, 'core/checkout-page.html', context=context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            street = form.cleaned_data['street']
            landmark = form.cleaned_data['landmark']
            country = form.cleaned_data['country']
            zip = form.cleaned_data['zip']
            same_bill_address = form.cleaned_data['same_bill_address']
            save_info = form.cleaned_data['save_info']
            payment_option = form.cleaned_data['payment_option']
            print(street,
                  landmark,
                  country,
                  zip,
                  same_bill_address,
                  save_info,
                  payment_option)
        return redirect("checkout")


@login_required
def add_to_cart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        course=course,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order course is in the order
        if order.courses.filter(course__slug=course.slug).exists():
            order_item.save()
            messages.info(request, "This Course is already in your cart")
            return redirect('order-summary')
        else:
            messages.info(request, "This course is added to your cart")
            order.courses.add(order_item)
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                     ordered_date=ordered_date)
        order.courses.add(order_item)
        messages.success(request, "This course is added to your cart")
    return redirect('order-summary')


@login_required
def remove_from_cart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order course is in the order
        if order.courses.filter(course__slug=course.slug).exists():
            order_course = OrderItem.objects.get(
                course=course,
                user=request.user,
                ordered=False,
            )
            order.courses.remove(order_course)
            messages.success(request, "This course is removed from your cart")
            # delete order object if no courses associated  with current order
            if order.courses.count() == 0:
                order.delete()
                return redirect('order-summary')
            return redirect('order-summary')
        else:
            messages.warning(request, "This course is not in your cart")
            # TODO: Redirect to all courses page
            # return redirect("products", slug=slug)

            return redirect('/')
    else:
        messages.error(request, "You do not have an active order.")
        return redirect('order-summary')


@login_required
def remove_item_from_cart(request, slug):
    course = get_object_or_404(Course, slug=slug)
    order_qs = Order.objects.filter(user=request.user,
                                    ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if order course is in the order
        if order.course.filter(course__slug=course.slug).exists():
            order_item = OrderItem.objects.get(
                course=course,
                user=request.user,
                ordered=False,
            )
            order.courses.remove(order_item)
            messages.success(request, "This course is removed from your cart")
            return redirect('order-summary')
        else:
            messages.warning(request, "This course is not in your cart")
            return redirect("order-summary")
    else:
        messages.error(request, "You do not have an active order.")
        return redirect('order-summary')


class SearchResultsView(ListView):
    model = Course
    template_name = 'search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        object_list = Course.objects.filter(Q(title__icontains=query))
        return object_list
