import typing
from merrill.item import Item

from datetime import date

def consolidate_items(items: typing.List[Item]):
    '''
        Consolidate a list of `Item` into a list of `Item` where each `Item` has been merged with any other `Item` with the 
        same `item_description`, where the new `Item` has a `serial_numbers` list that is the union of the `serial_numbers` 
        lists of the original `Item`s. This new list of serial numbers will be sorted alphanumerically.
        
        The `quantity` of the new `Item` is the sum of the `quantity` of the original `Item`s.

        Returns a new list of `Item` objects that have been consolidated.
    '''
    consolidated_items = []
    for item in items:
        if item.item_description not in [i.item_description for i in consolidated_items]:
            consolidated_items.append(item)
        else:
            for i in consolidated_items:
                if i.item_description == item.item_description:
                    i.serial_numbers = sorted(i.serial_numbers + item.serial_numbers)
                    i.quantity += item.quantity
    return consolidated_items

def today_as_army_date():
    '''
        Return today's date as a string in the format 'DD MMM YY'.
    '''
    today = date.today()
    return today.strftime('%d %b %y').upper()