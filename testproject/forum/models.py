from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(AbstractUser):
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])

    REQUIRED_FIELDS = ['email', 'age']


class Comment(models.Model):
    text = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='comments')

    def __str__(self):
        return self.text[:10]