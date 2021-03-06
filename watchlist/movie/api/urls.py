from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.movies, name="movies"),
    path("movies/<int:pk>/", views.movie_detail, name="movie-detail"),
    path("streams/", views.Stream.as_view(), name="streams"),
    path("streams/<int:pk>/", views.StreamDetail.as_view(), name="stream-detail"),
    path("reviews/", views.ReviewList.as_view(), name="reviews"),
    path("reviews/<int:pk>/", views.ReviewDetail.as_view(), name="review-detail"),
    path("movies/reviews/<str:username>/", views.UserReviews.as_view(), name="user-reviews"),
    path("movies/reviews/", views.QueryUserReviews.as_view(), name="query-user-reviews"),
    path("movies/<int:pk>/reviews/", views.MovieReview.as_view(), name="movie-reviews"),
]
