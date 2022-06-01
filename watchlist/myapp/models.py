from django.db import models
from django.utils.translation import gettext as _


class Occupant(models.Model):
    name = models.CharField(_("Name"), max_length=255)

    def __str__(self) -> str:
        return self.name


class House(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    occupants = models.ManyToManyField("myapp.Occupant", verbose_name=_("occupants"), related_name="houses")

    def __str__(self) -> str:
        return self.name
