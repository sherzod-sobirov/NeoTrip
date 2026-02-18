from django import forms
from .models import Contact, Comment
from django.core.validators import MinLengthValidator


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'comment']
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
