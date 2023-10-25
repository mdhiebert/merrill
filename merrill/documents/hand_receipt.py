import typing

from merrill.item import Item
from merrill.util import consolidate_items

from PyPDF2 import PdfReader, PdfWriter

class HandReceipt:
    '''
        A Python class that represents a DA Form 2062.
    '''

    def __init__(self, 
                 name_from: str, name_to: str, hand_receipt_number: str, 
                 end_item_stock_number: str, end_item_description: str,
                 publication_number: str, publication_date: str, quantity: int,
                 items: typing.List[Item]
                 ):
        self.name_from = name_from
        self.name_to = name_to
        self.hand_receipt_number = hand_receipt_number
        self.end_item_stock_number = end_item_stock_number
        self.end_item_description = end_item_description
        self.publication_number = publication_number
        self.publication_date = publication_date
        self.quantity = quantity

        self.items = self._sanitize_items(items)

    def _validate_items(self, items: typing.List[Item]):
        assert isinstance(items, list), 'items must be a list'
        return items
    
    def _sanitize_items(self, items: typing.List[Item]):
        items = self._validate_items(items)

        return consolidate_items(items)
    
    def _calculate_number_of_pages(self):
        num_of_items = len(self.items)

        if num_of_items <= 16:
            return 1
        elif num_of_items <= 37:
            return 2
        else:
            return 2 + ((num_of_items - 37) // 21) + 1

    
    def write_to_pdf(self, base_filepath: str, filepath: str,):
        '''
            Write the contents of this `HandReceipt` object to a PDF file at the given `filepath`.

            TODO lots of redundant code, could be cleaned up.
        '''
        reader = PdfReader(base_filepath)
        page_1 = reader.pages[0]
        page_2 = reader.pages[1]

        expected_number_of_pages = self._calculate_number_of_pages()

        writer = PdfWriter()
        writer.add_page(page_1)

        updated_dict = {}

        for i,item in enumerate(self.items[:16]):
            index = i

            if index == 0:
                updated_dict[f'ITEMDESA[0]'] = item.formatted_str
                updated_dict[f'QTYAUTHA[0]'] = 'ea'
                updated_dict[f'QTYAA[0]'] = item.quantity
            else:
                updated_dict[f'ITEMDESA_{index}[0]'] = item.formatted_str
                updated_dict[f'QTYAUTHA_{index}[0]'] = 'ea'
                updated_dict[f'QTYAA_{index}[0]'] = item.quantity

        updated_dict['FROM[0]'] = self.name_from
        updated_dict['TO[0]'] = self.name_to
        updated_dict['ITEMDES[0]'] = self.end_item_description
        updated_dict['PAGE[0]'] = 1
        updated_dict['OFPG[0]'] = expected_number_of_pages

        writer.update_page_form_field_values(
            writer.pages[0], updated_dict
        )

        updated_dict = {}
        writer.add_page(page_2)

        # if there are more than 16 items in items
        if len(self.items) > 16:

            for i,item in enumerate(self.items[16:37]):
                index = i

                if index == 0:
                    updated_dict[f'ITEMDESB[0]'] = item.formatted_str
                    updated_dict[f'QTYAUTHB[0]'] = 'ea'
                    updated_dict[f'QTYAB[0]'] = item.quantity
                else:
                    updated_dict[f'ITEMDESB_{index}[0]'] = item.formatted_str
                    updated_dict[f'QTYAUTHB_{index}[0]'] = 'ea'
                    updated_dict[f'QTYAB_{index}[0]'] = item.quantity

            updated_dict['PAGEA[0]'] = 2
            updated_dict['OFPGA[0]'] = expected_number_of_pages

            writer.update_page_form_field_values(
                writer.pages[1], updated_dict
            )

        # write the first document
        with open(filepath, "wb") as output_stream:
            writer.write(output_stream)

        # if there are more than 37 items in items

        if len(self.items) > 37:
            reader = PdfReader(base_filepath)
            page_1 = reader.pages[1]

            writer = PdfWriter()
            writer.add_page(page_1)

            updated_dict = {}

            for page_number,start_index in enumerate(range(37, len(self.items), 21)):
                for i,item in enumerate(self.items[start_index:start_index + 21]):
                    index = i

                    if index == 0:
                        updated_dict[f'ITEMDESB[0]'] = item.formatted_str
                        updated_dict[f'QTYAUTHB[0]'] = 'ea'
                        updated_dict[f'QTYAB[0]'] = item.quantity
                    else:
                        updated_dict[f'ITEMDESB_{index}[0]'] = item.formatted_str
                        updated_dict[f'QTYAUTHB_{index}[0]'] = 'ea'
                        updated_dict[f'QTYAB_{index}[0]'] = item.quantity

                updated_dict['PAGEA[0]'] = page_number + 3
                updated_dict['OFPGA[0]'] = expected_number_of_pages

                writer.update_page_form_field_values(
                    writer.pages[0], updated_dict
                )

                filepath = filepath.replace('.pdf', f'_EXTRA_PAGE_{page_number + 1}.pdf')

                with open(filepath, "wb") as output_stream:
                    writer.write(output_stream)
