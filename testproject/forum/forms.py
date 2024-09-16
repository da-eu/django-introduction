from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def check_username(username):
    if not username.isalnum() or not username.isascii():
        raise ValidationError(_('usernameにはアルファベットと数字のみ入力可能です'))
    if not username[0].isalpha():
        raise ValidationError(_('usernameの最初の文字はアルファベットにしてください'))

class RegisterForm(forms.Form):
    username = forms.CharField(validators=[check_username])
    email = forms.EmailField()
    age = forms.IntegerField(min_value=0, max_value=200)

class PostForm(forms.Form):
    text = forms.CharField()