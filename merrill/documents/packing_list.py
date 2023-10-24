import typing
from PyPDF2 import PdfReader, PdfWriter

from merrill.item import Item
from merrill.util import consolidate_items


class PackingList:

    def __init__(self, packed_by: str, number_of_boxes: int, requisition_number: str, order_number: str,
                 end_item: str, date: str, page_number: int, total_pages: int, items: typing.List[Item]):
        self.packed_by = packed_by
        self.number_of_boxes = number_of_boxes
        self.requisition_number = requisition_number
        self.order_number = order_number
        self.end_item = end_item
        self.date = date
        self.page_number = page_number
        self.total_pages = total_pages
        self.items = self._sanitize_items(items)

    def _validate_items(self, items: typing.List[Item]):
        assert isinstance(items, list), 'items must be a list'
        return items
    
    def _sanitize_items(self, items: typing.List[Item]):
        items = self._validate_items(items)

        return consolidate_items(items)
    
    def write_to_pdf(self, base_filepath: str, filepath: str):
        '''
            Write the contents of this `PackingList` object to a PDF file at the given `filepath`.
        '''
        reader = PdfReader(base_filepath)
        page_1 = reader.pages[0]

        writer = PdfWriter()
        writer.add_page(page_1)

        updated_dict = {}

        for i,item in enumerate(self.items):
            index = i + 1

            updated_dict[f'contents_{index}'] = item.formatted_str
            updated_dict[f'unit_{index}'] = 'ea'
            updated_dict[f'init_{index}'] = item.quantity
            updated_dict[f'total_{index}'] = item.quantity

        updated_dict['PACKED_BY'] = self.packed_by
        updated_dict['3_END_ITEM'] = self.end_item
        updated_dict['certname'] = self.packed_by

        writer.update_page_form_field_values(
            writer.pages[0], updated_dict
        )

        with open(filepath, "wb") as output_stream:
            writer.write(output_stream)
