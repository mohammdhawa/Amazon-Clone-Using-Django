from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from utils.generate_code import generate_code
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile')
    code = models.CharField(max_length=10, default=generate_code)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


PHONE_TYPE_CHOICES = (
    ('Primary', 'Primary'),
    ('Secondary', 'Secondary'),
)


class ContactNumber(models.Model):
    user = models.ForeignKey(User, related_name='contact_number', on_delete=models.CASCADE)
    phone_type = models.CharField(max_length=10, choices=PHONE_TYPE_CHOICES)
    number = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.user} - number: {self.number}"


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
