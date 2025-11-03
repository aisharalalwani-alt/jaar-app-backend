from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    PostListCreateView, PostDetailView,
    EventListCreateView, EventDetailView,
    VolunteerListCreateView, VolunteerDetailView,
    NeighborListCreateView, JoinEventView, SignupUserView, LogoutView, MyNeighborProfileView,
)

urlpatterns = [
    # Posts
    path('posts/', PostListCreateView.as_view(), name='posts_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Events
    path('events/', EventListCreateView.as_view(), name='events_list_create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

    # Volunteers
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteers_list_create'),
    path('volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer_detail'),

    # Neighbors
    path('neighbors/', NeighborListCreateView.as_view(), name='neighbors_list_create'),
    path('join-event/<int:event_id>/', JoinEventView.as_view(), name='join-event'),
    path('my-profile/', MyNeighborProfileView.as_view(), name='my_neighbor_profile'),



    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupUserView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
]
 