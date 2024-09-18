from django.db import models

class User(models.Model):
    username = models.CharField(max_length=32)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return self.username

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comments')
    text = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]