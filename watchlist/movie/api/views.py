from rest_framework.decorators import api_view
from rest_framework.response import Response
from watchlist.movie.models import Movie

from .serializers import MovieSerializer

@api_view(["GET"])
def movie_list(request):
    """
    List all movies.
    """
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)
