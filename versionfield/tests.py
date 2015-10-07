from __future__ import unicode_literals

import unittest

from django.test import TestCase
from django.db import models

from . import VersionField
from .constants import DEFAULT_NUMBER_BITS
from .version import Version


class DummyModel(models.Model):
    version = VersionField()


class VersionFieldTest(TestCase):

    def setUp(self):
        DummyModel.objects.create(version="0.1")
        DummyModel.objects.create(version="1.0")
        DummyModel.objects.create(version="1.0.1")

    def test_get_by_exact_version(self):
        thing = DummyModel.objects.get(version="0.1")
        self.assertEqual(thing.version, "0.1")
        self.assertEqual(thing.version, "0.1.0")

    def test_filter_by_greater_than_version(self):
        things = DummyModel.objects.filter(version__gt="0.1")
        self.assertEqual(len(things), 2)

        things = DummyModel.objects.filter(version__gt="1.0")
        self.assertEqual(len(things), 1)

        things = DummyModel.objects.filter(version__gt="1.0.1")
        self.assertEqual(len(things), 0)

    def test_filter_by_less_than_version(self):
        things = DummyModel.objects.filter(version__lt="0.1")
        self.assertEqual(len(things), 0)

        things = DummyModel.objects.filter(version__lt="1.0")
        self.assertEqual(len(things), 1)

        things = DummyModel.objects.filter(version__lt="1.0.1")
        self.assertEqual(len(things), 2)

    def test_overflow_number(self):
        error_occured = False
        try:
            DummyModel.objects.create(version="1.999.1")
        except ValueError:
            error_occured = True
        self.assertTrue(error_occured)


class DummyModelCustomBit(models.Model):
    version = VersionField(number_bits=(8, 16, 8))


class VersionFieldCustomBitsTest(TestCase):
    def setUp(self):
        DummyModelCustomBit.objects.create(version="1.999.1")

    def test_get_by_exact_version(self):
        thing = DummyModelCustomBit.objects.get(version="1.999.1")
        self.assertEqual(thing.version, "1.999.1")


class VersionObjectTestCase(unittest.TestCase):

    def test_equal_operator(self):
        self.assertEqual(
            Version("1.2.3", DEFAULT_NUMBER_BITS),
            Version("1.2.3", DEFAULT_NUMBER_BITS),
        )

    def test_lt_operator(self):
        self.assertTrue(
            Version("1.2.3", DEFAULT_NUMBER_BITS) <
            Version("1.2.4", DEFAULT_NUMBER_BITS)
        )
        self.assertFalse(
            Version("1.2.4", DEFAULT_NUMBER_BITS) <
            Version("1.2.3", DEFAULT_NUMBER_BITS)
        )

    def test_le_operator(self):
        self.assertTrue(
            Version("1.2.3", DEFAULT_NUMBER_BITS) <=
            Version("1.2.4", DEFAULT_NUMBER_BITS)
        )
        self.assertTrue(
            Version("1.2.4", DEFAULT_NUMBER_BITS) <=
            Version("1.2.4", DEFAULT_NUMBER_BITS)
        )

    def test_gt_operator(self):
        self.assertTrue(
            Version("1.2.4", DEFAULT_NUMBER_BITS) >
            Version("1.2.3", DEFAULT_NUMBER_BITS)
        )
        self.assertFalse(
            Version("2.3.4", DEFAULT_NUMBER_BITS) >
            Version("3.2.1", DEFAULT_NUMBER_BITS)
        )

    def test_ge_operator(self):
        self.assertTrue(
            Version("1.2.4", DEFAULT_NUMBER_BITS) >=
            Version("1.2.3", DEFAULT_NUMBER_BITS)
        )
        self.assertTrue(
            Version("3.3.3", DEFAULT_NUMBER_BITS) <=
            Version("3.3.3", DEFAULT_NUMBER_BITS)
        )
