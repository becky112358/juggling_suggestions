from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Pattern


class PatternModelTests(TestCase):

    def test_invalid_siteswap(self):
        """
        A validation error is raised if the user attempts to create a pattern
        with an invalid siteswap.
        """

        invalid_siteswaps = [
            '1&2&3',
            '1234',
        ]

        for i in range(len(invalid_siteswaps)):
            self.assertRaises(ValidationError,
                              Pattern(siteswap=invalid_siteswaps[i], prop_type=Pattern.PropType.BALL).full_clean)


