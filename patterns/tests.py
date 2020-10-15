from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Pattern


class PatternModelTests(TestCase):

    def test_invalid_siteswap(self):
        """
        A validation error is raised if the user attempts to create a pattern
        with an invalid siteswap.
        """
        self.assertRaises(ValidationError, Pattern(siteswap='1234', prop_type=Pattern.PropType.BALL).full_clean)


