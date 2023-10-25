from PyPDF2 import PdfReader, PdfWriter

from merrill import CONFIG

reader = PdfReader(CONFIG.PDF_2062_FILEPATH)
print(reader.get_form_text_fields())
