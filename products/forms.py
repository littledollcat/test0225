from django import forms
from django.forms import ModelForm
from .models import Orders, Products


class OrderForm(forms.Form):
    
    products = [(str(p.id), p.id) for p in Products.objects.all()]
    
    product_id = forms.DecimalField(
        widget = forms.Select(choices=products)
    )
    
    qty = forms.DecimalField()
    CustomerID = forms.DecimalField()
    vip = forms.BooleanField(required=False)
    
    



