from django.db import models
from django.contrib.auth.models import User

# Create your models here.

Address_TYPE_CHOICES = (
    ('Home', 'Home'),
    ('Work', 'Work'),
    ('Office', 'Office'),
    ('Other', 'Other')
)


class Adress(models.Model):
    user = models.ForeignKey(User, related_name='user_address', on_delete=models.CASCADE)
    address = models.TextField(max_length=500)
    address_type = models.CharField(max_length=10, choices=Address_TYPE_CHOICES)

    def __str__(self):
        return str(self.user) + " address"
