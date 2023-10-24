import typing
import re

class Item:

    @staticmethod
    def from_str(s: str):
        '''
            Create a new `Item` object from a string.
            This should be a string that was created by calling `str()` on an `Item` object.
        '''

        pattern = re.compile(r'(?P<quantity>\d+)x\s+(?P<description>.+)\s+\((?P<serials>((.+)(,\s*.+)*)?)\)')
        match = pattern.match(s)

        if match is None: raise ValueError('Invalid input - string does not match expected format (e.g. "2x Apple iPhone (1234, 5678)")')

        quantity = int(match.group('quantity'))
        description = match.group('description')
        serials = match.group('serials').split(',')

        return Item(description, serials, quantity)

    def __init__(self, item_description: str, serial_numbers: typing.List[str], quantity: int):
        self.item_description = item_description
        self.serial_numbers = self._sanitize_serial_numbers(serial_numbers)
        self.quantity = quantity

        if self.quantity < 0: raise ValueError('Invalid quantity - must be greater than or equal to 0')

    def _sanitize_serial_numbers(self, serial_numbers: typing.List[str]):
        assert isinstance(serial_numbers, list), 'serial_numbers must be a list'
        return list(sorted([sn.strip() for sn in serial_numbers if sn]))

    def __str__(self):
        return f'{self.quantity}x {self.item_description} ({", ".join(self.serial_numbers)})'
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Item):
            return False
        return self.item_description == __value.item_description and self.serial_numbers == __value.serial_numbers and self.quantity == __value.quantity
    
    @property
    def formatted_str(self):
        if len(self.serial_numbers) > 0:
            return f'{self.item_description} (S/N: {", ".join(self.serial_numbers)})'
        else:
            return f'{self.item_description}'