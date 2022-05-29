from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.movies, name="movies"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("streams/", views.Stream.as_view(), name="streams"),
    path("streams/<int:pk>/", views.StreamDetail.as_view(), name="stream_detail"),
]
