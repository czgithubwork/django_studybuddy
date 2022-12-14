from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=30, unique=True, null=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=False, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Room(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=False)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)    

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.body[0:50]


