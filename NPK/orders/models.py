# Create your models here.
from django.contrib.auth.models import User
from django.db import models

# from django.db.models import SlugField


class Course(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField(blank=False)
    duration = models.CharField(max_length=10)
    slug = models.SlugField(max_length=80, unique=True)
    discount_price = models.FloatField(default=0, blank=True)
    description = models.TextField(max_length=1000, blank=False)
    Image = models.ImageField(upload_to='images', blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class FileIndex(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    media = models.FileField(upload_to='files', blank=False)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.course


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # item = models.ForeignKey(Item, on_delete=CASCADE)
    ordered = models.BooleanField(default=False)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False, )


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.OneToManyField(Course, on_delete=models.CASCADE)
    street = models.CharField(max_length=1000, blank=False)
    City = models.CharField(max_length=1000, blank=False)
    state = models.CharField(max_length=1000, blank=False)
    Country = models.CharField(max_length=1000, blank=False)
    pincode = models.CharField(max_length=1000, blank=False)
    mobile = models.CharField(max_length=1000, blank=False)

    def __str__(self):
        return f'{self.user.first_name}'
