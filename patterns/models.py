from enum import Enum

from django.db import models


class PropTypes(Enum):
    BALLS = 0
    CLUBS = 1
    RINGS = 2
    HATS = 3


class Modifier(Enum):
    NONE = 0
    MILLS_MESS = 1
    WHILE_BALANCING_A_CLUB_ON_THE_FACE = 2


class BodyThrow(Enum):
    BEHIND_THE_BACK = 0
    BEHIND_THE_SHOULDER = 1
    UNDER_THE_ARM = 2
    UNDER_THE_LEG = 3


class BodyThrowType(Enum):
    CATCH = 0
    THROW = 1
    CATCH_AND_THROW = 2


class Pattern(models.Model):
    # List of integers of base infinity
    siteswap = models.CharField(max_length=200)
    prop_type = PropTypes
    modifiers = models.JSONField(default=list)
    # Body throw should be a list of tuples
    # [(x, behind the back, throw), (y, under the leg, throw)]
    body_throw = models.JSONField(default=list)
    # User-unique information:
    # Date, number of catches

    def __str__(self):
        s = self.siteswap
        s += " " + str(self.prop_type)
        for m in self.modifiers:
            s += " " + str(m)
        for b in self.body_throw:
            s += " " + str(b)
        return s


class Difficulties(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    n_objects = models.PositiveIntegerField(default=20)
    max_height_minus_min_height = models.IntegerField(default=20)
    body_throw_difficulty = models.IntegerField(default=100)

    def __str__(self):
        return "\n              n objects: " + str(self.n_objects) \
              + "\nmax height - min height: " + str(self.max_height_minus_min_height) \
              + "\n  body throw difficulty: " + str(self.body_throw_difficulty)
