from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .siteswap import *


GOALS_MAX_COLUMNS = 3


class Pattern(models.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _, _, self.n_objects = siteswap_average(self.siteswap)
        self.max_height_minus_min_height = max_height_minus_min_height(self.siteswap)

    class PropType(models.TextChoices):
        BALL = 'ball', _('ball')
        CLUB = 'club', _('club')
        RING = 'ring', _('ring')

    n_jugglers = models.PositiveIntegerField(
        verbose_name="number of jugglers",
        default=1,
        validators=[MinValueValidator(1)]
    )
    n_objects = models.PositiveIntegerField(
        default=0,
        verbose_name="number of objects",
        editable=False
    )
    prop_type = models.CharField(
        max_length=5,
        choices=PropType.choices
    )
    siteswap = models.CharField(
        max_length=200,
        validators=[validate_siteswap_characters,
                    validate_siteswap_brackets,
                    validate_siteswap_integer_average]
    )

    max_height_minus_min_height = models.IntegerField(
        default=0,
        verbose_name="maximum height - minimum height",
        editable=False
    )
    body_throw_difficulty = models.IntegerField(
        default=0,
        verbose_name="Body throw difficulty "
                     "(0: no body throws, 100: maximum difficulty)",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        s = str(self.n_jugglers) + " juggler "
        s += str(self.n_objects)
        s += " " + self.prop_type
        s += " " + self.siteswap
        first = True
        if hasattr(self, 'bodythrow_set'):
            for b in self.bodythrow_set.all():
                if first:
                    first = False
                else:
                    s += ","
                s += " " + str(b)
        if hasattr(self, 'modifier'):
            if first:
                s += " "
            else:
                s += ", "
            s += str(self.modifier)
        return s


class BodyThrow(models.Model):

    class BodyThrowType(models.TextChoices):
        BEHIND_THE_BACK = 'behind the back', _('behind the back')
        BEHIND_THE_NECK = 'behind the neck', _('behind the neck')
        BEHIND_THE_SHOULDER = 'behind the shoulder', _('behind the shoulder')
        UNDER_THE_ARM = 'under the arm', _('under the arm')
        UNDER_THE_LEG = 'under the leg', _('under the leg')

    class BodyCatchOrThrow(models.TextChoices):
        CATCH = "caught", _('catch')
        THROW = "thrown", _('throw')
        CATCH_AND_THROW = "caught and thrown", _('catch and throw')

    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    throw_moment = models.CharField(
        max_length=1
    )
    throw_type = models.CharField(
        max_length=20,
        choices=BodyThrowType.choices
    )
    catch_or_throw = models.CharField(
        max_length=20,
        choices=BodyCatchOrThrow.choices
    )

    def __str__(self):
        return "with the " + self.throw_moment + " " + self.catch_or_throw + " " + self.throw_type


def add_modifier_text(modifier_present, modifier_name, s, first):
    if modifier_present:
        if first:
            first = False
        else:
            s += ", "
        s += modifier_name
    return s, first


class Modifier(models.Model):
    pattern = models.OneToOneField(Pattern, on_delete=models.CASCADE)

    mills_mess = models.BooleanField(verbose_name="Mill's mess")
    while_balancing_a_club_on_the_face = models.BooleanField()
    while_standing_on_a_rolla_bolla = models.BooleanField()

    def __str__(self):
        first = True
        s = ""
        s, first = add_modifier_text(self.mills_mess, Modifier.mills_mess.field.verbose_name, s, first)
        s, first = add_modifier_text(self.while_balancing_a_club_on_the_face,
                                     Modifier.while_balancing_a_club_on_the_face.field.verbose_name, s, first)
        s, first = add_modifier_text(self.while_standing_on_a_rolla_bolla,
                                     Modifier.while_standing_on_a_rolla_bolla.field.verbose_name, s, first)
        return s


class Goal(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    row = models.IntegerField(validators=[MinValueValidator(0)])
    column = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(GOALS_MAX_COLUMNS)])

    def __str__(self):
        return str(self.pattern)


class Record(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    number_of_catches = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    date = models.DateField()
    user1 = models.ForeignKey(get_user_model(),
                              on_delete=models.CASCADE,
                              related_name='primary_user')
    user2 = models.ForeignKey(get_user_model(),
                              verbose_name='Other juggler',
                              on_delete=models.CASCADE,
                              null=True,
                              related_name='partner_user1')

    def __str__(self):
        return str(self.date) + " : " + str(self.number_of_catches) + " catches"

