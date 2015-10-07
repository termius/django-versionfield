import six

from django.utils.encoding import python_2_unicode_compatible

from .utils import convert_version_string_to_int, convert_version_int_to_string


@python_2_unicode_compatible
class Version(object):
    def __init__(self, string, number_bits):
        """
        Take in a verison string e.g. '3.0.1'
        Store it as a converted int
        """
        self.number_bits = number_bits
        self.internal_integer = convert_version_string_to_int(
            string, number_bits)

    def __str__(self):
        return six.text_type(convert_version_int_to_string(
                             self.internal_integer, self.number_bits))

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return self.internal_integer

    def __eq__(self, other):
        if not other:
            return False  # we are obviously a valid Version, but 'other' isn't
        if isinstance(other, six.string_types):
            other = Version(other, self.number_bits)
        return int(self) == int(other)

    def __lt__(self, other):
        if not other:
            return False
        if isinstance(other, six.string_types):
            other = Version(other, self.number_bits)
        return int(self) < int(other)

    def __le__(self, other):
        if not other:
            return False
        if isinstance(other, six.string_types):
            other = Version(other, self.number_bits)
        return int(self) <= int(other)

    def __gt__(self, other):
        if not other:
            return False
        if isinstance(other, six.string_types):
            other = Version(other, self.number_bits)
        return int(self) > int(other)

    def __ge__(self, other):
        if not other:
            return False
        if isinstance(other, six.string_types):
            other = Version(other, self.number_bits)
        return int(self) >= int(other)
