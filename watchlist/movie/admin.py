from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "release_date", "active"]
    list_filter = ["release_date", "active"]
    search_fields = ["title", "relase_date"]
    ordering = ["-release_date"]
