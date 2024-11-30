from django import forms
from .models import Pizza
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100,min_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100,min_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    address = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        return password

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")
        if confirm_password != password:
            raise ValidationError("Password and confirm password do not match.")
        return confirm_password

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'size', 'crust', 'toppings']
        widgets = {
            'toppings': forms.CheckboxSelectMultiple,
        }

