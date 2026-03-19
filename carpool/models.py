from django.db import models
from accounts.models import User
from network.models import Node
from trips.models import Trip

class CarpoolRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    passenger = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='pickup_requests')
    dropoff_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='dropoff_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.username}: {self.pickup_node} → {self.dropoff_node}"

class DriverOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    carpool_request = models.ForeignKey(CarpoolRequest, on_delete=models.CASCADE, related_name='offers')
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    detour = models.IntegerField(default=0)
    fare = models.FloatField(default=0.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.driver.username} → {self.carpool_request}"

