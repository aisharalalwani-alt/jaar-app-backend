from rest_framework import serializers
from .models import NeighborProfile, Post, Event, Volunteer

# NeighborProfile Serializer
class NeighborProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeighborProfile
        fields = '__all__'

# Post Serializer
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

# Event Serializer
class EventSerializer(serializers.ModelSerializer):
    volunteers = serializers.StringRelatedField(many=True, read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


# Volunteer Serializer
class VolunteerSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Event.objects.all()
    )

    class Meta:
        model = Volunteer
        fields = '__all__'