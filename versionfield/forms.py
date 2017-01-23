"""Custom form fields."""

import six

from django import forms

from .version import Version
from .constants import DEFAULT_NUMBER_BITS
from .utils import convert_version_int_to_string


class VersionField(forms.CharField):

    """A form field dedicated to version numbers."""

    def __init__(self, number_bits=DEFAULT_NUMBER_BITS, **kwargs):
        self.number_bits = number_bits
        return super(VersionField, self).__init__(**kwargs)

    def check_format(self, string):
        """Check that value contains no more than N decimal numbers."""
        parts = string.split(".")
        actual_len = len(parts)
        allowed_len = len(self.number_bits)
        if actual_len > allowed_len:
            raise forms.ValidationError(
                "Version has %(actual)d components; only %(allowed)d "
                "components are allowed",
                code="too_long_version",
                params=dict(actual=actual_len, allowed=allowed_len))
        for i, (part, bits) in enumerate(zip(parts, self.number_bits), 1):
            if not part.isdigit():
                raise forms.ValidationError(
                    "Version's %(index)d component (%(part)s) is not numeric; "
                    "only numeric values are allowed",
                    code="not_numeric_version",
                    params=dict(index=i, part=part))
            num = int(part)
            max_allowed = (1 << bits) - 1
            if num > max_allowed:
                raise forms.ValidationError(
                    "Version's %(index)d component (%(part)s) is too big; "
                    "maximum allowed value for this component is %(allowed)d",
                    code="version_component_too_big",
                    params=dict(index=i, part=part, allowed=max_allowed))

    def to_python(self, value):
        """Verifies that value can be converted to a Version object."""
        if not value:
            return None

        self.check_format(value)

        if isinstance(value, six.string_types):
            return Version(value, self.number_bits)

        return Version(
            convert_version_int_to_string(value, self.number_bits),
            self.number_bits
        )
