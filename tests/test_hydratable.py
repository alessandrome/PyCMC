import unittest
from PyCMC.models.hydratable import Hydratable


class TestHydratable(unittest.TestCase):

    def test_present_value(self):
        h = Hydratable(value=10, present=True)
        self.assertTrue(h.present)
        self.assertEqual(h.unwrap(), 10)
        self.assertTrue(h)

    def test_none_but_present(self):
        h = Hydratable(value=None, present=True)
        self.assertTrue(h.present)
        self.assertIsNone(h.unwrap())
        self.assertFalse(h)

    def test_not_present(self):
        h = Hydratable(value=None, present=False)
        self.assertFalse(h.present)
        self.assertEqual(h.unwrap(default=123), 123)
        self.assertFalse(h)

    def test_unwrap(self):
        h = Hydratable(value=10, present=False)
        self.assertEqual(h.unwrap(), None)
        self.assertEqual(h.unwrap(5), 5)
        h2 = Hydratable(value=5, present=True)
        self.assertEqual(h2.unwrap(), 5)
        self.assertEqual(h2.unwrap(10), 5)

    def test_get_value(self):
        h1 = Hydratable(value=10, present=True)
        self.assertEqual(h1.get_value(), 10)
        h2 = Hydratable(value=10, present=False)
        with self.assertRaises(ValueError):
            h2.get_value()

    def test_dehydrate(self):
        h = Hydratable(value=10, present=True)
        self.assertEqual(h.unwrap(5), 10)
        h.dehydrate()
        self.assertEqual(h.unwrap(5), 5)

    def test_set_value(self):
        h = Hydratable(value=None, present=False)
        self.assertEqual(h.unwrap(5), 5)
        h.set_value(10)
        self.assertEqual(h.unwrap(5), 10)
        h.set_value(20, present=False)
        self.assertEqual(h.unwrap(5), 5)

    def test_arithmetic_operations(self):
        h = Hydratable(value=10, present=True)
        self.assertEqual(h + 5, 15)
        self.assertEqual(h - 3, 7)
        self.assertEqual(h * 2, 20)
        self.assertEqual(h / 2, 5.0)

    def test_operator_error_when_value_is_none(self):
        h = Hydratable(value=None, present=True)
        with self.assertRaises(TypeError):
            _ = h + 1

    def test_attribute_access(self):
        class Dummy:
            def __init__(self):
                self.foo = 'bar'

        h = Hydratable(value=Dummy(), present=True)
        self.assertEqual(h.foo, 'bar')

    def test_repr(self):
        h1 = Hydratable(value=10, present=True)
        self.assertEqual(repr(h1), "Hydratable(10)")
        h2 = Hydratable(value=None, present=False)
        self.assertEqual(repr(h2), "Hydratable(<not hydrated>)")
        h3 = Hydratable(value=50, present=False)
        self.assertEqual(repr(h3), "Hydratable(<not hydrated>)")

    def test_equality(self):
        h1 = Hydratable(value=5, present=True)
        h2 = Hydratable(value=5, present=True)
        h3 = Hydratable(value=5, present=False)
        h4 = Hydratable(value=10, present=True)
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
        self.assertNotEqual(h1, h4)


if __name__ == '__main__':
    unittest.main()
