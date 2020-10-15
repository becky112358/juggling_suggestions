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


def validate_siteswap_brackets(siteswap):
    ok = True
    sync_throw = False
    sync_throw_found_comma = False
    multiplex_throw = False
    for i in range(len(siteswap)):
        if siteswap[i] == '(':
            sync_throw = True
            if multiplex_throw:
                ok = False
        elif siteswap[i] == '[':
            multiplex_throw = True
            if i >= len(siteswap) - 3:
                ok = False
            elif not siteswap[i+1].isdigit() and not siteswap[i+1].isalpha():
                ok = False
            elif not siteswap[i+2].isdigit() and not siteswap[i+2].isalpha():
                ok = False
        elif siteswap[i] == ']':
            if not multiplex_throw:
                ok = False
            multiplex_throw = False
        elif siteswap[i] == ')':
            if multiplex_throw:
                ok = False
            if not sync_throw_found_comma:
                ok = False
            sync_throw = False
            sync_throw_found_comma = False
        elif siteswap[i] == ',':
            sync_throw_found_comma = True
            if not sync_throw:
                ok = False
            elif multiplex_throw:
                ok = False
            elif i == len(siteswap) - 1:
                ok = False
            elif not siteswap[i-1].isdigit() and not siteswap[i-1].isalpha():
                ok = False
            elif not siteswap[i+1].isdigit() and not siteswap[i+1].isalpha():
                ok = False
        elif siteswap[i] == '*':
            if i != len(siteswap) - 1:
                ok = False
            elif len(siteswap) == 1:
                ok = False
            elif siteswap[i-1] != ')':
                ok = False

    if multiplex_throw:
        ok = False
    if sync_throw:
        ok = False

    if not ok:
        raise ValidationError(
            _('%(siteswap)s contains bracket problems'),
            params={'siteswap': siteswap},
        )


def siteswap_average(siteswap):
    n_throws = 0
    total = 0
    sync_throw = False
    multiplex_throw = False
    for s in siteswap:
        if s == '(':
            sync_throw = True
        elif sync_throw:
            if s == ',':
                n_throws += 1
            elif s == ')':
                n_throws += 1
                sync_throw = False
        elif s == '[':
            n_throws += 1
            multiplex_throw = True
        elif multiplex_throw:
            if s == ']':
                multiplex_throw = False
        elif s != '*':
            n_throws += 1

        # TODO Provide support beyond base 36
        if s.isdigit() or (s.isalpha() and s != 'x'):
            total += int(s, base=36)

    average = int(total / n_throws)

    return n_throws, total, average


def validate_siteswap_integer_average(siteswap):
    n_throws, total, _unused = siteswap_average(siteswap)
    average_is_integer = (n_throws > 0) and (total % n_throws == 0)

    if not average_is_integer:
        raise ValidationError(
            _('%(siteswap)s has a non-integer average'),
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
        validators=[validate_siteswap_characters,
                    validate_siteswap_brackets,
                    validate_siteswap_integer_average]
    )
    prop_type = models.CharField(
        max_length=5,
        choices=PropType.choices
    )

    # User-unique information:
    # Date, number of catches

    def __str__(self):
        s = ""
        if hasattr(self, 'difficulty'):
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


def max_height_minus_min_height(siteswap):
    max_height = 0
    min_height = 100
    for s in siteswap:
        if s.isdigit() or s.isalpha() and s != 'x':
            number = int(s, base=36)
            if number > max_height:
                max_height = number
            if number < min_height:
                min_height = number
    return max_height - min_height


class Difficulty(models.Model):
    pattern = models.OneToOneField(Pattern, on_delete=models.CASCADE)
    n_objects = models.PositiveIntegerField(verbose_name="number of objects",
                                            editable=False)
    max_height_minus_min_height = models.IntegerField(verbose_name="maximum height - minimum height",
                                                      editable=False)
    body_throw_difficulty = models.IntegerField(default=100)

    class Meta:
        verbose_name_plural = "Difficulty"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'pattern'):
            _, _, self.n_objects = siteswap_average(self.pattern.siteswap)
            self.max_height_minus_min_height = max_height_minus_min_height(self.pattern.siteswap)

    def __str__(self):
        return "\n              n objects: " + str(self.n_objects) \
              + "\nmax height - min height: " + str(self.max_height_minus_min_height) \
              + "\n  body throw difficulty: " + str(self.body_throw_difficulty)
