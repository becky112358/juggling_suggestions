from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def siteswap_character_is_throw(s):
    throw = False
    if s.isdigit():
        throw = True
    # TODO sometimes x is a throw
    elif s.isalpha() and s != 'x':
        throw = True
    return throw


def siteswap_character_height(s):
    height = 0
    if s.isdigit():
        height = int(s)
    elif s.isalpha():
        if s.islower():
            height = ord(s) - ord('a') + 10
        else:
            height = ord(s) - ord('A') + 36
    return height


def validate_siteswap_characters(siteswap):
    for s in siteswap:
        if siteswap_character_is_throw(s):
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
            elif not siteswap_character_is_throw(siteswap[i+1]) and not siteswap_character_is_throw(siteswap[i+2]):
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
            elif not siteswap_character_is_throw(siteswap[i-1]) and not siteswap_character_is_throw(siteswap[i+1]):
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

        if siteswap_character_is_throw(s):
            total += siteswap_character_height(s)

    if n_throws == 0:
        average = 0
    else:
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


def max_height_minus_min_height(siteswap):
    max_height = 0
    min_height = 100
    for s in siteswap:
        if siteswap_character_is_throw(s):
            height = siteswap_character_height(s)
            if height > max_height:
                max_height = height
            if height < min_height:
                min_height = height
    return max_height - min_height


class Record(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE)
    user_or_team = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_catches = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    date = models.DateField()

