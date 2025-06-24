from django.forms import ModelForm
from .models import Product
from django.forms import Textarea
from django import forms
from .models import Product
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'discount', 'image', 'data', 'category']
        widgets = {
            'description': Textarea(attrs={'rows': 4, 'cols': 40}),
            'data': Textarea(attrs={'rows': 2, 'cols': 40}),
        }

        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control'
            })