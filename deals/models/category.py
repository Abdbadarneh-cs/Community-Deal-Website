from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    # descr = models.CharField(max_length=100,blank=True)
    def __str__(self):
        return self.name