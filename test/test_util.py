import unittest

from merrill.item import Item
from merrill.util import consolidate_items

# write test cases for merrill/util.py here
class TestUtil(unittest.TestCase):
    
    def test_consolidate_items_small_list_with_overlap(self):

        item_list = [
            Item('item_description_1', ['A123'], 1),
            Item('item_description_2', ['B123'], 2),
            Item('item_description_3', ['C123'], 3),
            Item('item_description_1', ['A124'], 1),
        ]

        consolidated_item_list = consolidate_items(item_list)

        self.assertEqual(len(consolidated_item_list), 3)
        self.assertEqual(consolidated_item_list[0].formatted_str, 'item_description_1 (S/N: A123, A124)')

    def test_consolidate_items_medium_list_with_overlap(self):

        item_list = [
            Item('item_description_1', ['A123'], 1),
            Item('item_description_2', ['B123'], 2),
            Item('item_description_3', ['C123'], 3),
            Item('item_description_1', ['A124'], 1),
            Item('item_description_2', ['B124'], 2),
            Item('item_description_3', ['C124'], 3),
        ]

        consolidated_item_list = consolidate_items(item_list)

        self.assertEqual(len(consolidated_item_list), 3)
        self.assertEqual(consolidated_item_list[0].formatted_str, 'item_description_1 (S/N: A123, A124)')
        self.assertEqual(consolidated_item_list[1].formatted_str, 'item_description_2 (S/N: B123, B124)')
        self.assertEqual(consolidated_item_list[2].formatted_str, 'item_description_3 (S/N: C123, C124)')

    def test_consolidate_items_large_list_with_overlap(self):

        item_list = [
            Item('item_description_1', ['A123'], 1),
            Item('item_description_2', ['B123'], 2),
            Item('item_description_3', ['C123'], 3),
            Item('item_description_1', ['A124'], 1),
            Item('item_description_2', ['B124'], 2),
            Item('item_description_3', ['C124'], 3),
            Item('item_description_1', ['A125'], 1),
            Item('item_description_2', ['B125'], 2),
            Item('item_description_3', ['C125'], 3),
        ]

        consolidated_item_list = consolidate_items(item_list)

        self.assertEqual(len(consolidated_item_list), 3)
        self.assertEqual(consolidated_item_list[0].formatted_str, 'item_description_1 (S/N: A123, A124, A125)')
        self.assertEqual(consolidated_item_list[1].formatted_str, 'item_description_2 (S/N: B123, B124, B125)')
        self.assertEqual(consolidated_item_list[2].formatted_str, 'item_description_3 (S/N: C123, C124, C125)')

        # test empty list
        item_list = []
        consolidated_item_list = consolidate_items(item_list)
        self.assertEqual(len(consolidated_item_list), 0)

    def test_consolidate_items_large_list_with_overlap_and_empty_items(self):

        # test list with empty items
        item_list = [
            Item('item_description_1', ['A123'], 1),
            Item('item_description_2', ['B123'], 2),
            Item('item_description_3', ['C123'], 3),
            Item('item_description_1', ['A124'], 1),
            Item('item_description_2', ['B124'], 2),
            Item('item_description_3', ['C124'], 3),
            Item('item_description_1', ['A125'], 1),
            Item('item_description_2', ['B125'], 2),
            Item('item_description_3', ['C125'], 3),
            Item('', [], 0),
            Item('', [], 0),
            Item('', [], 0),
        ]

        consolidated_item_list = consolidate_items(item_list)

        self.assertEqual(len(consolidated_item_list), 4)
        self.assertEqual(consolidated_item_list[0].formatted_str, 'item_description_1 (S/N: A123, A124, A125)')
        self.assertEqual(consolidated_item_list[1].formatted_str, 'item_description_2 (S/N: B123, B124, B125)')
        self.assertEqual(consolidated_item_list[2].formatted_str, 'item_description_3 (S/N: C123, C124, C125)')

    def test_consolidate_items_large_list_with_no_overlap(self):

        # test list where no items are consolidated
        item_list = [
            Item('item_description_1', ['A123'], 1),
            Item('item_description_2', ['B123'], 2),
            Item('item_description_3', ['C123'], 3),
            Item('item_description_4', ['D123'], 1),
            Item('item_description_5', ['E123'], 2),
            Item('item_description_6', ['F123'], 3),
            Item('item_description_7', ['G123'], 1),
            Item('item_description_8', ['H123'], 2),
            Item('item_description_9', ['I123'], 3),
        ]

        consolidated_item_list = consolidate_items(item_list)

        self.assertEqual(len(consolidated_item_list), 9)
        self.assertEqual(consolidated_item_list[0].formatted_str, 'item_description_1 (S/N: A123)')
        self.assertEqual(consolidated_item_list[1].formatted_str, 'item_description_2 (S/N: B123)')
        self.assertEqual(consolidated_item_list[2].formatted_str, 'item_description_3 (S/N: C123)')
        self.assertEqual(consolidated_item_list[3].formatted_str, 'item_description_4 (S/N: D123)')
        self.assertEqual(consolidated_item_list[4].formatted_str, 'item_description_5 (S/N: E123)')
        self.assertEqual(consolidated_item_list[5].formatted_str, 'item_description_6 (S/N: F123)')
        self.assertEqual(consolidated_item_list[6].formatted_str, 'item_description_7 (S/N: G123)')
        self.assertEqual(consolidated_item_list[7].formatted_str, 'item_description_8 (S/N: H123)')
        self.assertEqual(consolidated_item_list[8].formatted_str, 'item_description_9 (S/N: I123)')



if __name__ == '__main__':
    unittest.main()