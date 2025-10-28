from django.urls import path
from .views import (
    PostListCreateView, PostDetailView,
    EventListCreateView, EventDetailView,
    VolunteerListCreateView, VolunteerDetailView,
    NeighborListCreateView, NeighborDetailView,
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
    path('api/neighbors/<int:pk>/', NeighborDetailView.as_view(), name='neighbor_detail'),
]
