from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("watchlist.movie.api.urls")),
    path("api/account/", include("watchlist.user_app.api.urls")),
]
