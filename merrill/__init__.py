import typing

from merrill.item import Item
from merrill.util import today_as_army_date

from merrill.documents.hand_receipt import HandReceipt
from merrill.documents.packing_list import PackingList
from merrill.documents.hazardous_declaration import HazardousDeclaration

from merrill.constants import CONFIG
class Merrill:

    @staticmethod
    def from_text(text: str):
        '''
            Create a `Merill` object from a text file.
        '''
        admin_data,items = text.split('--------------------------------------------------------------------------------')

        _,overall_description,hand_receipt_from,hand_receipt_to,packed_by,_ = admin_data.split('\n')
        overall_description = overall_description.split(':')[1].strip()
        hand_receipt_from = hand_receipt_from.split(':')[1].strip()
        hand_receipt_to = hand_receipt_to.split(':')[1].strip()
        packed_by = packed_by.split(':')[1].strip()

        raw_boxes = items.split('#')
        boxes_of_items = []

        for raw_box in raw_boxes:
            raw_items = raw_box.split('\n')
            items = []

            for raw_item in raw_items:
                if raw_item.strip() == '':
                    continue

                items.append(Item.from_str(raw_item))

            boxes_of_items.append(items)
        
        return Merrill(
            overall_description = overall_description,
            hand_receipt_from = hand_receipt_from,
            hand_receipt_to = hand_receipt_to,
            packed_by = packed_by,
            boxes_of_items = boxes_of_items
        )

    def __init__(self,
                    overall_description: str,

                    # 2062 Admin Information
                    hand_receipt_from: str, hand_receipt_to: str,

                    # 1750 Admin Information
                    packed_by: str,

                    boxes_of_items: typing.List[typing.List[Item]]
                ):
        self.overall_description = overall_description

        self.hand_receipt_from = hand_receipt_from
        self.hand_receipt_to = hand_receipt_to

        self.packed_by = packed_by

        self.boxes_of_items = boxes_of_items

    def generate_paperwork(self, output_directory = 'output'):

        for i,box in enumerate(self.boxes_of_items):
            box_number = i + 1

            # Generate 2062s
            hr = HandReceipt(
                name_from = self.hand_receipt_from, 
                name_to = self.hand_receipt_to, 
                hand_receipt_number = None, end_item_stock_number = None, 
                end_item_description = self.overall_description, 
                publication_number = None, publication_date = None, quantity = None, 
                items = box
            )
            
            hr.write_to_pdf(CONFIG.PDF_2062_FILEPATH, f'{output_directory}/2062_{box_number}.pdf')

            # Generate 1750s
            pl = PackingList(
                packed_by = self.packed_by,
                number_of_boxes = len(self.boxes_of_items),
                requisition_number = None, order_number = None,
                end_item = self.overall_description,
                date = today_as_army_date(),
                page_number = None, total_pages = None,
                items = box,
                box_number = box_number
            )
            
            pl.write_to_pdf(CONFIG.PDF_1750_FILEPATH, f'{output_directory}/1750_{box_number}.pdf')

            hazardous_items_in_box = [item for item in box if item.is_hazardous]
            
            if len(hazardous_items_in_box) > 0:
                hd = HazardousDeclaration(
                    shipper = CONFIG.SHIPPER_ADDRESS,
                    shipper_phone_number = None,
                    dsn = None,
                    air_waybill_number = None,
                    page_number = None,
                    total_pages = None,
                    shipper_reference_number_tcn = None,
                    consignee = CONFIG.CONSIGNEE_INFORMATION,
                    is_exclusive_to_cargo_aircraft = None,
                    airport_of_departure = CONFIG.AIRPORT_OF_DEPARTURE,
                    destination_airport = CONFIG.DESTINATION_AIRPORT,
                    is_radioactive = None,
                    unit_id_number = None,
                    proper_shipping_name = None,
                    class_or_division = None,
                    packing_group = None,
                    quantity_and_type_of_packing = None,
                    packing_instructions = None,
                    authorization = None,
                    additional_handling_information = CONFIG.ADDITIONAL_INFO,
                    emergency_telephone_number = CONFIG.EMERGENCY_CONTACT_INFO,
                    name_of_signatory = CONFIG.CEMA_HMO,
                    place_and_date = CONFIG.PLACE_OF_SIGNATURE + f'\n{today_as_army_date().upper()}',
                    items = hazardous_items_in_box
                )

                hd.write_to_pdf(CONFIG.PDF_HAZDEC_FILEPATH, f'{output_directory}/HAZDEC_{box_number}.pdf')
