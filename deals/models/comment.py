from django.db import models
from .user import User
from .deal import Deal

class Comment(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} on {self.deal.title}"
