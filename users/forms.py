from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': ' '
            })


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    email = forms.EmailField(max_length=254, required=True, label="Email")
    phone = forms.CharField(required=True, label="Phone Number")


    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': ' '
            })

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone Number must be contain only numbers")
        return phone


