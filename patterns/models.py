from enum import Enum

from django.db import models


PROP_TYPE_CHOICES = (
    ('BALL', 'ball'),
    ('CLUB', 'club'),
    ('RING', 'ring'),
)


#  class PropType(Enum):
#      BALLS = "ball"
#      CLUBS = "club"
#      RINGS = "ring"


class Modifier(Enum):
    MILLS_MESS = "Mills' mess"
    WHILE_BALANCING_A_CLUB_ON_THE_FACE = "while balancing a club on the face"


class BodyThrow(Enum):
    BEHIND_THE_BACK = "behind the back"
    BEHIND_THE_SHOULDER = "behind the shoulder"
    UNDER_THE_ARM = "under the arm"
    UNDER_THE_LEG = "under the leg"


class BodyThrowType(Enum):
    CATCH = "catch"
    THROW = "throw"
    CATCH_AND_THROW = "catch and throw"


class Pattern(models.Model):
    # TODO should be a list of integers of base 62
    siteswap = models.CharField(max_length=200)
    prop_type = models.CharField(
        max_length=5,
        choices=PROP_TYPE_CHOICES)
    modifiers = models.JSONField(
        default=list,
        choices=[(tag, tag.value) for tag in Modifier])
    # Body throw should be a list of tuples
    # [(x, behind the back, throw), (y, under the leg, throw)]
    body_throw = models.JSONField(
        default=list,
        choices=[(tag, tag.value) for tag in BodyThrow])
#  int(base=62),  # TODO should be a selection from siteswap
#  [(tag, tag.value) for tag in BodyThrowType]))
    # User-unique information:
    # Date, number of catches

    def __str__(self):
        s = str(self.difficulty.n_objects)
        s += " " + self.prop_type
        s += " " + self.siteswap
        for m in self.modifiers:
            s += " " + m
        for b in self.body_throw:
            s += " " + b
        return s


class Difficulty(models.Model):
    pattern = models.OneToOneField(Pattern, on_delete=models.CASCADE)
    n_objects = models.PositiveIntegerField(default=20,
                                            verbose_name="number of objects")
    max_height_minus_min_height = models.IntegerField(default=20,
                                                      verbose_name="maximum height - minimum height")
    body_throw_difficulty = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = "Difficulty"

    def __str__(self):
        return "\n              n objects: " + str(self.n_objects) \
              + "\nmax height - min height: " + str(self.max_height_minus_min_height) \
              + "\n  body throw difficulty: " + str(self.body_throw_difficulty)
