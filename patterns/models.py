from enum import Enum

from django.db import models


class Pattern(models.Model):
    siteswap = models.CharField(max_length=200)
    # User-unique information:
    # Date, number of catches


class PropTypes(Enum):
    BALLS = 0
    CLUBS = 1
    RINGS = 2


class Difficulties(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    n_objects = models.PositiveIntegerField(default=20)
    max_height_minus_min_height = models.IntegerField(default=20)
    prop_type = PropTypes
    body_throw_difficulty = models.IntegerField(default=100)
