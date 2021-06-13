from django.contrib import admin
from orders.models import Course, OrderItem, Order
# Register your models here.
admin.site.register(Course)


@admin.register(OrderItem)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['course', ]


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered_date', 'ordered']