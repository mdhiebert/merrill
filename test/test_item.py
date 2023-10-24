import unittest
from merrill.item import Item

class TestItem(unittest.TestCase):

    def test_from_str(self):
        item_str = '2x Apple iPhone (1234, 5678)'
        item = Item.from_str(item_str)
        self.assertEqual(item.item_description, 'Apple iPhone')
        self.assertEqual(item.serial_numbers, ['1234', '5678'])
        self.assertEqual(item.quantity, 2)

    def test_init(self):
        item = Item('Apple iPhone', ['1234', '5678'], 2)
        self.assertEqual(item.item_description, 'Apple iPhone')
        self.assertEqual(item.serial_numbers, ['1234', '5678'])
        self.assertEqual(item.quantity, 2)

    def test_str(self):
        item = Item('Apple iPhone', ['1234', '5678'], 2)
        self.assertEqual(str(item), '2x Apple iPhone (1234, 5678)')

    def test_eq(self):
        item1 = Item('Apple iPhone', ['1234', '5678'], 2)
        item2 = Item('Apple iPhone', ['1234', '5678'], 2)
        item3 = Item('Samsung Galaxy', ['1234', '5678'], 2)
        self.assertEqual(item1, item2)
        self.assertNotEqual(item1, item3)

    def test_formatted_str(self):
        item1 = Item('Apple iPhone', ['1234', '5678'], 2)
        item2 = Item('Apple iPhone', [], 2)
        self.assertEqual(item1.formatted_str, 'Apple iPhone (S/N: 1234, 5678)')
        self.assertEqual(item2.formatted_str, 'Apple iPhone')

    def test_from_str_invalid_input(self):
        with self.assertRaises(ValueError):
            Item.from_str('2x Apple iPhone (1234, 5678')

    def test_from_str_invalid_quantity(self):
        with self.assertRaises(ValueError):
            Item.from_str('2.5x Apple iPhone (1234, 5678)')

    def test_init_invalid_quantity(self):
        with self.assertRaises(ValueError):
            Item('Apple iPhone', ['1234', '5678'], -2)

    def test_str_no_serial_numbers(self):
        item = Item('Apple iPhone', [], 2)
        self.assertEqual(str(item), '2x Apple iPhone ()')

    def test_eq_invalid_type(self):
        item = Item('Apple iPhone', ['1234', '5678'], 2)
        self.assertNotEqual(item, 'Apple iPhone')

    def test_eq_different_quantity(self):
        item1 = Item('Apple iPhone', ['1234', '5678'], 2)
        item2 = Item('Apple iPhone', ['1234', '5678'], 3)
        self.assertNotEqual(item1, item2)

    def test_eq_different_serial_numbers(self):
        item1 = Item('Apple iPhone', ['1234', '5678'], 2)
        item2 = Item('Apple iPhone', ['1234', '9012'], 2)
        self.assertNotEqual(item1, item2)

    def test_formatted_str_no_item_description(self):
        item = Item('', ['1234', '5678'], 2)
        self.assertEqual(item.formatted_str, ' (S/N: 1234, 5678)')

    def test_formatted_str_no_serial_numbers(self):
        item = Item('Apple iPhone', [], 2)
        self.assertEqual(item.formatted_str, 'Apple iPhone')

if __name__ == '__main__':
    unittest.main()