from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework.decorators import APIView, api_view
from rest_framework.response import Response
from watchlist.movie.models import Movie, StreamingPlatform

from .serializers import MovieSerializer, StreamingPlatformSerializer


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
