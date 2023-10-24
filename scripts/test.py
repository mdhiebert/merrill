from PyPDF2 import PdfReader

from merrill.item import Item
from merrill.documents.hand_receipt import HandReceipt
from merrill.documents.packing_list import PackingList
from merrill.documents.hazardous_declaration import HazardousDeclaration

hr = HandReceipt('ME', 'YOU', None, None, 'TSO Loadout', None, None, None, [
    Item('Thing A', ['123', '456'], 2),
    Item('Thing B', ['789', '012', '456'], 3),
    Item('Thing A', ['145', '257'], 2),
    Item('Thing D', ['CRAZY-SERIAL-1', 'CRAZY-SERIAL-2'], 2),
])

hr.write_to_pdf('test.pdf')

pl = PackingList(
    'ME', None, None, None, 'TSO Loadout', None, None, None, [
        Item('Thing A', ['123', '456'], 2),
        Item('Thing B', ['789', '012', '456'], 3),
        Item('Thing A', ['145', '257'], 2),
        Item('Thing D', ['CRAZY-SERIAL-1', 'CRAZY-SERIAL-2'], 2),
    ]
)

pl.write_to_pdf('test2.pdf')

hd = HazardousDeclaration(None, None, None, None, None, None, 
                          None, None, True, None, False, None,
                          None, None, None, None, None, None, None, None,
                          None, None)
hd.write_to_pdf('test3.pdf')