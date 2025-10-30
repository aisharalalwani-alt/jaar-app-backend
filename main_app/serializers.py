from rest_framework import serializers
from .models import NeighborProfile, Post, Event, Volunteer

# ------------------ NEIGHBOR ------------------
class NeighborProfileSerializer(serializers.ModelSerializer):
    # Show the username of the user, read-only
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = NeighborProfile
        fields = ['id', 'user', 'house_number', 'street', 'phone', 'bio']
        read_only_fields = ['id', 'user']


# ------------------ POST ------------------
class PostSerializer(serializers.ModelSerializer):
    # Show the username of the creator, read-only
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    # Automatically assign current user when creating a post
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# ------------------ VOLUNTEER ------------------
class VolunteerSerializer(serializers.ModelSerializer):
    # Represent events by their id
    events = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Event.objects.all()
    )

    class Meta:
        model = Volunteer
        fields = ['id', 'name', 'phone', 'events']
        read_only_fields = ['id']


# ------------------ EVENT ------------------
class EventNestedVolunteerSerializer(serializers.ModelSerializer):
    # Nested serializer for volunteers in event
    class Meta:
        model = Volunteer
        fields = ['id', 'name', 'phone']


class EventSerializer(serializers.ModelSerializer):
    # Show creator username and nested volunteers
    created_by = serializers.StringRelatedField(read_only=True)
    volunteers = EventNestedVolunteerSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'created_by', 'volunteers']
        read_only_fields = ['id', 'created_by', 'volunteers']

    # Automatically assign current user as event creator
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
