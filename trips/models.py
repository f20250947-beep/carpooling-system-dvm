
from django.db import models
from accounts.models import User
from network.models import Node

class Trip(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    start_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='trips_started')
    end_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='trips_ended')
    max_passengers = models.IntegerField(default=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')

    def __str__(self):
        return f"{self.driver.username}: {self.start_node} → {self.end_node}"

class TripRoute(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='route')
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    order = models.IntegerField()
    is_passed = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.trip} - {self.node} ({self.order})"