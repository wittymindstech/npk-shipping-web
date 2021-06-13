from django import forms
from django.forms import ChoiceField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_OPTIONS = (
    ('U', 'UPI'),
    ('D', 'Debit Card'),
    ('C', 'Credit Card'),
)


class CheckoutForm(forms.Form):
    street = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control',
    }), max_length=120)
    landmark = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control',
    }), max_length=120, required=False)
    country = CountryField(blank_label='Select Country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': "custom-select d-block w-100",
            # 'id': "country"
        },)
    )
    zip = forms.IntegerField(widget=forms.TextInput(attrs={
        'placeholder': '123456',
        'class': 'form-control',
    }), )
    same_bill_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(choices=PAYMENT_OPTIONS, widget=forms.RadioSelect())
