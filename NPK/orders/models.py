# Create your models here.
from django.contrib.auth.models import User
from django.db import models
from django_countries.fields import CountryField
from django.shortcuts import reverse


# from django.db.models import SlugField


class Course(models.Model):
    title = models.CharField(max_length=120)
    price = models.FloatField(blank=False)
    duration = models.CharField(max_length=10)
    slug = models.SlugField(max_length=80, unique=True)
    discount_price = models.FloatField(default=0, blank=True)
    description = models.TextField(max_length=1000, blank=False)
    image = models.ImageField(upload_to='images', blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        pass

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return super().save(force_insert=force_insert, force_update=force_update, using=using,
                            update_fields=update_fields)

    def get_absolute_url(self):
        return reverse("core:products", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart(self):
        return reverse("core:add_to_cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart(self):
        return reverse("core:remove_from_cart", kwargs={
            'slug': self.slug
        })


class FileIndex(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    media = models.FileField(upload_to='files', blank=False)
    created_on = models.DateTimeField()

    def __str__(self):
        return self.course


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        return f"{self.course}"

    @property
    def get_total_value(self):
        return self.quantity * self.course.price

    @property
    def get_discount_value(self):
        return self.course.discount_price

    @property
    def get_amount_saved(self):
        return self.get_total_value() - self.get_discount_value()

    @property
    def get_final_price(self):
        if self.course.discount_price:
            return self.get_discount_value()
        else:
            return self.get_total_value()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False, )

    class Meta:
        pass

    def __str__(self):
        return f"{self.user.username}  {self.ordered_date}"

    @property
    def get_total(self):
        total = 0
        for order_courses in self.courses.all():
            total += order_courses.get_final_price()
        return total


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, )
    street = models.CharField(max_length=100, blank=False)
    City = models.CharField(max_length=50, blank=False)
    state = models.CharField(max_length=50, blank=False)
    Country = models.CharField(max_length=50, blank=False)
    pincode = models.CharField(max_length=8, blank=False)
    mobile = models.CharField(max_length=15, blank=False)

    def __str__(self):
        return f'{self.user.first_name}'
