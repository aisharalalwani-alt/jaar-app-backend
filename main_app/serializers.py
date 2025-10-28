from rest_framework import serializers
from .models import NeighborProfile, Post, Event, Volunteer

class NeighborProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeighborProfile
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'
