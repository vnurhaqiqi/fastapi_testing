import unittest

from .main import *


class TestFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_reformat_product_name(self):
        new_product_name = reformat_product_name("Lenovo X Series")

        self.assertEqual(new_product_name,
                         "{}-{}".format("LENOVO", len(fake_db)))

    def test_reformat_product_empty_name(self):
        new_product_name = reformat_product_name("")

        self.assertEqual(new_product_name, "default-name")
