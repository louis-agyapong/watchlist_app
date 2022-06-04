import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class StreamingPlatform(models.Model):
    name = models.CharField(_("Name"), max_length=255, unique=True)
    about = models.TextField(_("About"), blank=True)
    website = models.URLField(_("URL"), max_length=255)

    class Meta:
        verbose_name = _("Streaming Platform")
        verbose_name_plural = _("Streaming Platforms")

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    release_date = models.DateField(_("Release date"), blank=True, null=True)
    platform = models.ForeignKey(
        "movie.StreamingPlatform",
        verbose_name=_("Platform"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="movies",
    )
    average_rating = models.FloatField(_("Average Rating"), default=0)
    number_ratings = models.PositiveIntegerField(_("Number of ratings"), default=0)
    active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def clean(self) -> None:
        if len(self.title) < 3:
            raise ValidationError(
                _("Title must be at least 3 characters long."),
                code="title_too_short",
            )

        if self.title == self.description:
            raise ValidationError(
                _("Title and Description should be different."),
                code="title_description_same",
            )

        if self.release_date > datetime.date.today():
            raise ValidationError(_("Release date cannot be in the future."), code="release_date_future")

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    movie = models.ForeignKey(
        "movie.Movie",
        verbose_name=_("Movie"),
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    user = models.ForeignKey(User, verbose_name=_("User"), on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.PositiveSmallIntegerField(_("Rating"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(_("Description"), blank=True)
    active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self) -> str:
        return f"{self.movie.title} - {str(self.rating)}/5"
