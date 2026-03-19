from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PASSENGER = 'passenger'
    DRIVER = 'driver'

    ROLE_CHOICES = [
        (PASSENGER, 'Passenger'),
        (DRIVER, 'Driver'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=PASSENGER
    )

    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='accounts_users'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='accounts_users'
    )

    def is_driver(self):
        return self.role == self.DRIVER

    def is_passenger(self):
        return self.role == self.PASSENGER
    
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('topup', 'Top Up'),
        ('fare_deduct', 'Fare Deduction'),
        ('earning', 'Driver Earning'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    trip = models.ForeignKey('trips.Trip', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - ₹{self.amount}"   