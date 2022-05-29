from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Movie(models.Model):
    title = models.CharField(_("Title"), max_length=100)
    description = models.TextField(_("Description"), blank=True)
    release_date = models.DateField(_("Release date"), blank=True, null=True)
    active = models.BooleanField(_("Active"), default=True)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)

    def clean(self) -> None:
        if len(self.title) < 4:
            raise ValidationError(
                _("Title must be at least 3 characters long."),
                code="title_too_short",
            )

    def __str__(self) -> str:
        return self.title
