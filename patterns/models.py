from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_siteswap_characters(siteswap):
    for s in siteswap:
        if s.isdigit():
            continue
        elif s.isalpha():
            continue
        elif s in ['(', ')', '[', ']', '*', ',']:
            continue
        else:
            raise ValidationError(
                _('%(siteswap)s contains invalid siteswap characters'),
                params={'siteswap': siteswap},
            )


class Pattern(models.Model):

    class PropType(models.TextChoices):
        BALL = 'ball', _('ball')
        CLUB = 'club', _('club')
        RING = 'ring', _('ring')

    # TODO should be a list of integers of base 62
    siteswap = models.CharField(
        max_length=200,
        validators=[validate_siteswap_characters]
    )
    prop_type = models.CharField(
        max_length=5,
        choices=PropType.choices
    )

    # User-unique information:
    # Date, number of catches

    def __str__(self):
        s = str(self.difficulty.n_objects)
        s += " " + self.prop_type
        s += " " + self.siteswap
        # TODO fixme
        if hasattr(self, 'body_throw'):
            s += " " + str(self.body_throw)
        if hasattr(self, 'modifier'):
            s += " " + str(self.modifier)
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


class Modifier(models.Model):
    pattern = models.OneToOneField(Pattern, on_delete=models.CASCADE)

    mills_mess = models.BooleanField(verbose_name="Mill's mess")
    while_balancing_a_club_on_the_face = models.BooleanField()
    while_standing_on_a_rolla_bolla = models.BooleanField()

    def __str__(self):
        # TODO eek duplicate code
        s = ""
        if self.mills_mess:
            s += "Mills' mess"
        if self.while_balancing_a_club_on_the_face:
            if s != "":
                s += ", "
            s += "while balancing a club on the face"
        if self.while_standing_on_a_rolla_bolla:
            if s != "":
                s += ", "
            s += "while standing on a rolla bolla"
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
