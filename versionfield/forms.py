"""Custom form fields."""

import six

from django import forms

from .version import Version
from .constants import DEFAULT_NUMBER_BITS
from .utils import convert_version_int_to_string


class VersionField(forms.IntegerField):

    """A form field dedicated to version numbers."""

    def __init__(self, number_bits=DEFAULT_NUMBER_BITS, **kwargs):
        self.number_bits = number_bits
        return super(VersionField, self).__init__(**kwargs)

    def to_python(self, value):
        """
        Verifies that value can be converted to a Version object
        """
        if not value:
            return None

        if isinstance(value, six.string_types):
            return Version(value, self.number_bits)

        return Version(
            convert_version_int_to_string(value, self.number_bits),
            self.number_bits
        )
