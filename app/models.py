from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default='avatar.svg', upload_to='media')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topics(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Rooms(models.Model):
    name = models.CharField(max_length=200)
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE, related_name='room')
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Messages(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]