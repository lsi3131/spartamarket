from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    image = models.ImageField(upload_to='images/', blank=True)
    comment = models.TextField(default='')
    like_products = models.ManyToManyField(
        'items.Item', related_name="like_items"
    )
