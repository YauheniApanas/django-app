from django import forms
from django.contrib.auth.models import User, Group

from .models import Product, Order


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount'


class OrderForm(forms.ModelForm):
    class CustomMMCF(forms.ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return '%s' % obj.name

    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'products', 'user'
    products = CustomMMCF(
        queryset=Product.objects.filter(archived=False).all(),
        widget=forms.CheckboxSelectMultiple,
    )
