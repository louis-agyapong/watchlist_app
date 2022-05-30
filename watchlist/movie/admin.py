from django.contrib import admin

from .models import Movie, StreamingPlatform, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date", "active"]
    list_filter = ["release_date", "active"]
    search_fields = ["title", "relase_date"]
    ordering = ["-release_date"]


@admin.register(StreamingPlatform)
class StreamingPlatformAdmin(admin.ModelAdmin):
    list_display = ["name", "about", "website"]
    search_fields = ["name"]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["movie", "rating", "active"]
    list_filter = ["active"]
    search_fields = ["movie", "rating"]
    ordering = ["-active"]
