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
