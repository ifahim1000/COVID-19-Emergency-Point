from django import forms
from .models import Buyer, Provider

class SignUpFormBuyer(forms.ModelForm) :
    class Meta:
        model = Buyer
        fields = ['image',]
        labels = {
            'image' : ''
        }
        
class SignUpFormPro(forms.ModelForm) :
    class Meta:
        model = Provider
        fields = ['image',]
        labels = {
            'image' : ''
        }
        