from rest_framework import serializers
from .models import NeighborProfile, Post, Event, Volunteer

# ------------------ NEIGHBOR ------------------
class NeighborProfileSerializer(serializers.ModelSerializer):
    # Show the username of the user, read-only
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = NeighborProfile
        fields = ['id', 'user', 'house_number', 'postal_code',  'street', 'phone', 'bio']
        read_only_fields = ['id', 'user']


# ------------------ POST ------------------
class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'created_by', 'title', 'image','content', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user.neighborprofile
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
        fields = ['id', 'title', 'description', 'date', 'location', 'created_by', 'volunteers']
        read_only_fields = ['id', 'created_by', 'volunteers']

    def create(self, validated_data):
        request = self.context.get('request')
        neighbor = NeighborProfile.objects.get(user=request.user)
        validated_data['created_by'] = neighbor
        return super().create(validated_data)
