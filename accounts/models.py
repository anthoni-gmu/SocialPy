from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import os
from PIL import Image
from django.db.models.signals import post_save
# Create your models here.

class User(AbstractUser):
    stripe_customer_id=models.CharField(max_length=50)


class Profile(models.Model):
    

