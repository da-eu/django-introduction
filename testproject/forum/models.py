from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

def check_username(username):
    if not username.isalnum() or not username.isascii():
        raise ValidationError(_('usernameにはアルファベットと数字のみ入力可能です'))
    if not username[0].isalpha():
        raise ValidationError(_('usernameの最初の文字はアルファベットにしてください'))

class User(models.Model):
    username = models.CharField(max_length=32, validators=[check_username])
    email = models.EmailField()
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    
    def __str__(self):
        return self.username

class Comment(models.Model):
    text = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self):
        return self.text[:10]