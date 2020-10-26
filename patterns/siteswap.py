from django.core.exceptions import ValidationError
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
