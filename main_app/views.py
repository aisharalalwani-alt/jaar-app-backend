from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post, Event, Volunteer, NeighborProfile
from .serializers import PostSerializer, EventSerializer, VolunteerSerializer, NeighborProfileSerializer

# ------------------ POSTS ------------------
class PostListCreateView(APIView):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return Response({"message": f"Post {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ EVENTS ------------------
class EventListCreateView(APIView):
    def get(self, request):
        events = Event.objects.all().order_by('date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = get_object_or_404(Event, id=pk)
        event.delete()
        return Response({"message": f"Event {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ VOLUNTEERS ------------------
class VolunteerListCreateView(APIView):
    def get(self, request):
        volunteers = Volunteer.objects.all().order_by('-joined_at')
        serializer = VolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolunteerDetailView(APIView):
    def get(self, request, pk):
        volunteer = get_object_or_404(Volunteer, id=pk)
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    def put(self, request, pk):
        volunteer = get_object_or_404(Volunteer, id=pk)
        serializer = VolunteerSerializer(volunteer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        volunteer = get_object_or_404(Volunteer, id=pk)
        volunteer.delete()
        return Response({"message": f"Volunteer {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ NEIGHBORS ------------------
class NeighborListCreateView(APIView):
    def get(self, request):
        neighbors = NeighborProfile.objects.all()
        serializer = NeighborProfileSerializer(neighbors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = NeighborProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NeighborDetailView(APIView):
    def get(self, request, pk):
        neighbor = get_object_or_404(NeighborProfile, id=pk)
        serializer = NeighborProfileSerializer(neighbor)
        return Response(serializer.data)

    def put(self, request, pk):
        neighbor = get_object_or_404(NeighborProfile, id=pk)
        serializer = NeighborProfileSerializer(neighbor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        neighbor = get_object_or_404(NeighborProfile, id=pk)
        neighbor.delete()
        return Response({"message": f"Neighbor {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)
