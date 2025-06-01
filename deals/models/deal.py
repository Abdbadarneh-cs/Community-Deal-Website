from django.db import models
from .user import User 
from .category import Category


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