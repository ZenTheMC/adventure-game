from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Exits and other relationships can be added as needed

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

class PlayerState(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    inventory = models.ManyToManyField(Item, blank=True)
