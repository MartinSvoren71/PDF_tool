
from pdf2image import convert_from_path
import pytesseract

pdf_path = 'sample.pdf'

# convert the pdf to a list of images
pages = convert_from_path(pdf_path)

# initialize the text string
text = ""

# perform OCR on each page of the PDF
for page in pages:
    text += pytesseract.image_to_string(page)

# save the text to a file
with open("sample.txt", "w") as text_file:
    text_file.write(text)
