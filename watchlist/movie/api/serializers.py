import datetime

from rest_framework import serializers
from watchlist.movie.models import Movie, StreamingPlatform


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for the Movie model.
    """

    class Meta:
        model = Movie
        fields = ("id", "title", "description", "release_date", "active", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at", "id")

    def validate_title(self, value):
        """
        Field Level Validation
        Check if the title is at least 3 characters long.
        """
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value

    def validate(self, data):
        # Object Level validation
        if data["release_date"] > datetime.date.today():
            """
            Check if the release date is not in the future.
            """
            raise serializers.ValidationError("Release date cannot be in the future.")
        if data["title"] == data["description"]:
            """
            Check if the title and description are not the same.
            """
            raise serializers.ValidationError("Title and Description should be different.")
        return data


class StreamingPlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for the StreamingPlatform model.
    """

    movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = StreamingPlatform
        fields = ("id", "name", "about", "website", "movies")
        read_only_fields = ("id",)
