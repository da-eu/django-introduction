from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Comment

User = get_user_model()

class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [User.USERNAME_FIELD] + User.REQUIRED_FIELDS


class PostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea
        }