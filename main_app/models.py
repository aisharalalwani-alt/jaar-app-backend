from django.db import models
from django.contrib.auth.models import User

#  NeighborProfile
class NeighborProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house_number = models.CharField(max_length=10)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


#  Post
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='media/posts/', blank=True, null=True)
    created_by = models.ForeignKey(NeighborProfile, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Event
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(NeighborProfile, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return f"{self.title} ({self.date.date()})"


# Volunteer
class Volunteer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    events = models.ManyToManyField(Event, related_name='volunteers')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
