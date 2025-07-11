from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transport = models.CharField(max_length=50)
    meal = models.CharField(max_length=50)
    meat_amount = models.PositiveIntegerField(null=True, blank=True)
    energy = models.PositiveIntegerField()
    carbon_score = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s activity on {self.submitted_at.date()}"

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=5)  # 1 to 5 stars
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"

