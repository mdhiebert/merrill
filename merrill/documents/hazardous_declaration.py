from PyPDF2 import PdfReader, PdfWriter

from merrill.util import today_as_army_date

class HazardousDeclaration:

    def __init__(self, shipper: str, shipper_phone_number: str, dsn: str, 
                 air_waybill_number: str, page_number: int, total_pages: int, shipper_reference_number_tcn: str,
                 consignee: str, is_exclusive_to_cargo_aircraft: bool, airport_of_departure: str, destination_airport: str, is_radioactive: bool,
                 unit_id_number: str, proper_shipping_name: str, class_or_division: str, packing_group: str, quantity_and_type_of_packing: str,
                 packing_instructions: str, authorization: str, additional_handling_information: str, emergency_telephone_number: str,
                 name_of_signatory: str, place_and_date: str, items: list = None):
        self.shipper = shipper
        self.shipper_phone_number = shipper_phone_number
        self.dsn = dsn
        self.air_waybill_number = air_waybill_number
        self.page_number = page_number
        self.total_pages = total_pages
        self.shipper_reference_number_tcn = shipper_reference_number_tcn
        self.consignee = consignee
        self.is_exclusive_to_cargo_aircraft = is_exclusive_to_cargo_aircraft
        self.airport_of_departure = airport_of_departure
        self.destination_airport = destination_airport
        self.is_radioactive = is_radioactive
        self.unit_id_number = unit_id_number
        self.proper_shipping_name = proper_shipping_name
        self.class_or_division = class_or_division
        self.packing_group = packing_group

        self.quantity_and_type_of_packing = quantity_and_type_of_packing
        self.packing_instructions = packing_instructions
        self.authorization = authorization
        self.additional_handling_information = additional_handling_information
        self.emergency_telephone_number = emergency_telephone_number
        self.name_of_signatory = name_of_signatory
        self.place_and_date = place_and_date

        self.items = items if items else []
    
    def write_to_pdf(self, base_filepath: str, filepath: str):
        '''
            Write the contents of this `PackingList` object to a PDF file at the given `filepath`.
        '''
        original_filepath = filepath
        for i,item in enumerate(self.items):
            reader = PdfReader(base_filepath)
            page_1 = reader.pages[0]

            writer = PdfWriter()
            writer.add_page(page_1)

            updated_dict = {}

            updated_dict['TextField1[0]'] = self.shipper
            updated_dict['TextField8[0]'] = self.consignee
            
            if self.is_exclusive_to_cargo_aircraft:
                updated_dict['TextField9[0]'] = 'XXXX'
            else:
                updated_dict['TextField10[0]'] = 'XXXX'

            updated_dict['TextField11[0]'] = self.airport_of_departure
            updated_dict['TextField12[0]'] = self.destination_airport

            if self.is_radioactive:
                updated_dict['TextField14[0]'] = 'XXXXX'
            else:
                updated_dict['TextField15[0]'] = 'XXXXX'

            updated_dict['TextField17[0]'] = item.item_description
            updated_dict['TextField20[0]'] = f'{item.quantity}x'

            updated_dict['TextField23[0]'] = self.additional_handling_information

            updated_dict['TextField25[0]'] = self.name_of_signatory
            updated_dict['TextField26[0]'] = self.place_and_date

            writer.update_page_form_field_values(
                writer.pages[0], updated_dict
            )

            if i > 0:
                filepath = original_filepath.replace('.pdf', f'_{i + 1}.pdf')

            with open(filepath, "wb") as output_stream:
                writer.write(output_stream)