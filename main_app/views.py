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
        """List all posts ordered by creation date descending."""
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new post and automatically assign it to the current user."""
        neighbor = get_object_or_404(NeighborProfile, user=request.user)
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=neighbor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """Retrieve a single post by its ID."""
        post = get_object_or_404(Post, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update only title and content if the user owns the post."""
        post = get_object_or_404(Post, id=pk)
        if post.created_by.user != request.user:
            return Response(
                {"error": "You can only edit your own posts."},
                status=status.HTTP_403_FORBIDDEN
            )

         
        allowed_fields = {
            key: request.data[key]
            for key in ["title", "content"]
            if key in request.data
        }

        serializer = PostSerializer(
            post,
            data=allowed_fields,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete a post if the current user is the owner."""
        post = get_object_or_404(Post, id=pk)
        if post.created_by.user != request.user:
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
        Create a new event and automatically assign the creator (NeighborProfile).
        """
        # Get the NeighborProfile for the logged-in user
        neighbor = get_object_or_404(NeighborProfile, user=request.user)

        # Pass the event data
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Save event with NeighborProfile, not User
            serializer.save(created_by=neighbor)
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

        # ✅ Fix: Compare with event.created_by.user, not request.user
        if event.created_by.user != request.user:
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

        # ✅ Fix: Compare with event.created_by.user, not request.user
        if event.created_by.user != request.user:
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
        List all neighbors with the same street as the current user.
        """
        try:
            current_neighbor = NeighborProfile.objects.get(user=request.user)
            neighbors = NeighborProfile.objects.filter(postal_code=current_neighbor.postal_code).exclude(id=current_neighbor.id)
        except NeighborProfile.DoesNotExist:
             neighbors = NeighborProfile.objects.none()

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
 # ------------------ MY NEIGHBOR PROFILE ------------------ 
class MyNeighborProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the current user's profile along with their posts, 
        created events, and events they've joined.
        """
        # Get the profile of the currently logged-in user
        neighbor = get_object_or_404(NeighborProfile, user=request.user)
        profile_data = NeighborProfileSerializer(neighbor).data

        # Get posts created by this user
        posts = Post.objects.filter(created_by=neighbor)
        posts_data = PostSerializer(posts, many=True).data

        # Get events created by this user
        created_events = Event.objects.filter(created_by=neighbor)
        created_events_data = EventSerializer(created_events, many=True).data

        # Get events the user has joined
        volunteer_entries = Volunteer.objects.filter(
            name=neighbor.user.username
        ) | Volunteer.objects.filter(phone=neighbor.phone)

        joined_events = Event.objects.filter(volunteers__in=volunteer_entries).distinct()
        joined_events_data = EventSerializer(joined_events, many=True).data

        return Response({
            "profile": profile_data,
            "posts": posts_data,
            "created_events": created_events_data,
            "joined_events": joined_events_data
        })

    def put(self, request):
        """
        Update the profile of the currently logged-in user.
        """
        neighbor = get_object_or_404(NeighborProfile, user=request.user)
        serializer = NeighborProfileSerializer(neighbor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

 
 # ------------------ JOIN EVENT ------------------
class JoinEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        """
        Allow the authenticated user to join an event as a volunteer.
        """
        event = get_object_or_404(Event, id=event_id)
        profile = get_object_or_404(NeighborProfile, user=request.user)

        # Create or get existing volunteer record
        volunteer, created = Volunteer.objects.get_or_create(
            name=profile.user.username,
            phone=profile.phone,
        )
        volunteer.events.add(event)
        return Response({"message": "Joined the event successfully!"})

# ------------------ USER SIGNUP ------------------
class SignupUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Signup a new user and automatically create a NeighborProfile.
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

        #  Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Automatically create an empty NeighborProfile for this user
        NeighborProfile.objects.create(
            user=user,
            house_number="",
            street="",
            phone="",
            bio=""
        )

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'message': "Signup successful! Profile created."
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