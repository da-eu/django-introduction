from django import forms
from .models import User, Comment

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'age']

class PostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']

        widgets = {
            'text': forms.Textarea
        }