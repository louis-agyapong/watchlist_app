from http import HTTPStatus

from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import APIView, api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from watchlist.movie.models import Movie, Review, StreamingPlatform

from .permissions import ReviewUserOrReadOnly
from .serializers import MovieSerializer, ReviewSerializer, StreamingPlatformSerializer


@api_view(["GET", "POST"])
def movies(request):
    """
    List create movie.
    """
    if request.method == "GET":
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)
    if request.method == "POST":
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def movie_detail(request, pk):
    """
    Retrieve, update or delete a movie.
    """
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == "GET":
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    elif request.method == "DELETE":
        movie.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class Stream(APIView):
    """
    View to list all streaming platforms or create a new one.
    """

    def get(self, request):
        streaming_platforms = StreamingPlatform.objects.all()
        serializer = StreamingPlatformSerializer(streaming_platforms, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class StreamDetail(APIView):
    """
    View to retrieve, update or delete a streaming platform.
    """

    def get(self, request, pk):
        streaming_platform = get_object_or_404(StreamingPlatform, pk=pk)
        serializer = StreamingPlatformSerializer(streaming_platform)
        return Response(serializer.data)

    def put(self, request, pk):
        streaming_platform = get_object_or_404(StreamingPlatform, pk=pk)
        serializer = StreamingPlatformSerializer(streaming_platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def delete(self, request, pk):
        streaming_platform = get_object_or_404(StreamingPlatform, pk=pk)
        streaming_platform.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class UserReviews(APIView):
    """
    View to list all user reviews.
    """

    def get(self, request, username):
        user_reviews = get_list_or_404(Review, user__username=username)
        serializer = ReviewSerializer(user_reviews, many=True)
        return Response(serializer.data)


class ReviewList(APIView):
    """
    View to list all reviews or create a new one.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class ReviewDetail(APIView):
    """
    View to retrieve, update or delete a review.
    """

    permission_classes = [ReviewUserOrReadOnly]

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)

    def delete(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        review.delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class MovieReview(APIView):
    """
    Movie review list and create.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=HTTPStatus.OK)

    def post(self, request, pk):
        """ "
        create a new review for a movie with the given pk in the url.
        """
        movie = get_object_or_404(Movie, pk=pk)
        review_user = request.user
        review_queryset = Review.objects.filter(movie=movie, user=review_user)
        serializer = ReviewSerializer(data=request.data)

        if review_queryset.exists():
            return Response({"message": "You have already reviewed this movie."}, status=HTTPStatus.BAD_REQUEST)

        print(serializer.is_valid())

        if serializer.is_valid():
            if movie.number_ratings == 0:
                movie.average_rating = serializer.validated_data["rating"]
            else:
                movie.average_rating = (movie.average_rating + serializer.validated_data["rating"]) / 2
            movie.number_ratings = movie.number_ratings + 1
            movie.save()
            print(movie)
            serializer.save(movie=movie, user=review_user)
            return Response(serializer.data, status=HTTPStatus.CREATED)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)
