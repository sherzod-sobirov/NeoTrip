from django.forms import ModelForm, IntegerField
from django.contrib.auth.forms import UserCreationForm
from .models import User, Testimonial
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class TestimonialForm(ModelForm):
    stars = IntegerField(required=False)

    class Meta:
        model = Testimonial
        fields = ['text', "stars"]
        


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password", min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise ValidationError('Bu email allaqachon ishlatilgan!')
            return email