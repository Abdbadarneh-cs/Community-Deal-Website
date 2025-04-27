from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank = True)
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Deal(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    document = models.FileField(upload_to='document/', blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
 