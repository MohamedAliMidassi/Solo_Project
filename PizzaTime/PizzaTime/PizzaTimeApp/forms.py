from django import forms
from .models import Pizza

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'size', 'crust', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple,
        }
