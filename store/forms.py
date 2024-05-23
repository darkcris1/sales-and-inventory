from django import forms
from django.forms import ModelForm
from .models import Item

class ProductForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'expiry_date': forms.TextInput(     
                attrs={'type': 'date'} 
            )
        }
