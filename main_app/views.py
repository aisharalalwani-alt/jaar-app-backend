from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Event, Volunteer, NeighborProfile
from .serializers import PostSerializer, EventSerializer, VolunteerSerializer, NeighborProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated,  IsAdminUser 

# ------------------ POSTS ------------------
class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all posts ordered by creation date descending.
        Only authenticated users can view posts.
        """
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new post and automatically assign it to the current user.
        """
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # User is assigned in serializer's create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a single post by its ID.
        """
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a post if the current user is the owner.
        Partial updates allowed.
        """
        post = get_object_or_404(Post, id=pk)
        if post.user != request.user:
            return Response({"error": "You can only edit your own posts."}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a post if the current user is the owner.
        """
        post = get_object_or_404(Post, id=pk)
        if post.user != request.user:
            return Response({"error": "You can only delete your own posts."}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({"message": f"Post {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ EVENTS ------------------
class EventListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all events ordered by date ascending.
        """
        events = Event.objects.all().order_by('date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new event and automatically assign the creator.
        """
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # created_by is assigned in serializer's create()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a single event by ID, including nested volunteers.
        """
        event = get_object_or_404(Event, id=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update an event if the current user is the creator.
        Partial updates allowed.
        """
        event = get_object_or_404(Event, id=pk)
        if event.created_by != request.user:
            return Response({"error": "You can only edit your own events."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete an event if the current user is the creator.
        """
        event = get_object_or_404(Event, id=pk)
        if event.created_by != request.user:
            return Response({"error": "You can only delete your own events."}, status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response({"message": f"Event {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ VOLUNTEERS ------------------
class VolunteerListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all volunteers ordered by joined date descending.
        """
        volunteers = Volunteer.objects.all().order_by('-joined_at')
        serializer = VolunteerSerializer(volunteers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new volunteer.
        """
        serializer = VolunteerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VolunteerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a volunteer by ID.
        """
        volunteer = get_object_or_404(Volunteer, id=pk)
        serializer = VolunteerSerializer(volunteer)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a volunteer by ID. Partial updates allowed.
        """
        volunteer = get_object_or_404(Volunteer, id=pk)
        serializer = VolunteerSerializer(volunteer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a volunteer by ID.
        """
        volunteer = get_object_or_404(Volunteer, id=pk)
        volunteer.delete()
        return Response({"message": f"Volunteer {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ NEIGHBORS ------------------
class NeighborListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all neighbors.
        """
        neighbors = NeighborProfile.objects.all()
        serializer = NeighborProfileSerializer(neighbors, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a neighbor profile and assign it to the current user.
        """
        serializer = NeighborProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # user is assigned in serializer
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NeighborDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve a neighbor profile by ID.
        """
        neighbor = get_object_or_404(NeighborProfile, id=pk)
        serializer = NeighborProfileSerializer(neighbor)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a neighbor profile if the current user is the owner.
        Partial updates allowed.
        """
        neighbor = get_object_or_404(NeighborProfile, id=pk)
        if neighbor.user != request.user:
            return Response({"error": "You can only update your own profile."}, status=status.HTTP_403_FORBIDDEN)

        serializer = NeighborProfileSerializer(neighbor, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a neighbor profile if the current user is the owner.
        """
        neighbor = get_object_or_404(NeighborProfile, id=pk)
        if neighbor.user != request.user:
            return Response({"error": "You can only delete your own profile."}, status=status.HTTP_403_FORBIDDEN)

        neighbor.delete()
        return Response({"message": f"Neighbor {pk} deleted"}, status=status.HTTP_204_NO_CONTENT)


# ------------------ JOIN EVENT ------------------
class JoinEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        """
        Allow the current user to join an event as a volunteer.
        Creates a volunteer if not exists, and adds to the event.
        """
        event = get_object_or_404(Event, id=event_id)
        neighbor = get_object_or_404(NeighborProfile, user=request.user)

        volunteer, created = Volunteer.objects.get_or_create(
            name=neighbor.user.username,
            phone=neighbor.phone
        )

        if not volunteer.events.filter(id=event.id).exists():
            volunteer.events.add(event)
            volunteer.save()

        return Response({
            "message": f"{neighbor.user.username} joined {event.title} successfully!"
        }, status=status.HTTP_200_OK)

# ------------------ USER SIGNUP ------------------

class SignupUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Signup a new user.
        Required fields: username, password. Email is optional.
        """
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'error': "Please provide a username and password"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({
                'error': "Username already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }, status=status.HTTP_201_CREATED)
    
# ------------------ USER LOGOUT ------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()   
            return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

 # End of views.py