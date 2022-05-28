from rest_framework import serializers
from watchlist.movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """

    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "release_date",
            "active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at", "id")
