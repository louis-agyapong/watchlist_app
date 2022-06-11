from django.apps import AppConfig


class UserAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "watchlist.user_app"

    def ready(self) -> None:
        from watchlist.user_app.signals import create_auth_token
