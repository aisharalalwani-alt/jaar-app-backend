from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    PostListCreateView, PostDetailView,
    EventListCreateView, EventDetailView,
    VolunteerListCreateView, VolunteerDetailView,
    NeighborListCreateView, JoinEventView, SignupUserView, LogoutView,
)

urlpatterns = [
    # Posts
    path('api/posts/', PostListCreateView.as_view(), name='posts_list_create'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),

    # Events
    path('api/events/', EventListCreateView.as_view(), name='events_list_create'),
    path('api/events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),

    # Volunteers
    path('api/volunteers/', VolunteerListCreateView.as_view(), name='volunteers_list_create'),
    path('api/volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer_detail'),

    # Neighbors
    path('api/neighbors/', NeighborListCreateView.as_view(), name='neighbors_list_create'),
    path('api/events/<int:event_id>/join/', JoinEventView.as_view(), name='join_event'),

    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', SignupUserView.as_view(), name='signup'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]
