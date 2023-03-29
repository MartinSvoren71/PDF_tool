import os
from PyPDF2 import PdfReader
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

def create_index(index_dir, pdf_dir):
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True), path=ID(stored=True))
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)
    ix = create_in(index_dir, schema)

    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    writer = ix.writer()

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        pdf = PdfReader(pdf_path)
        content = ''
        for page_num in range(len(pdf.pages)):
            content += pdf.pages[page_num].extract_text()
        writer.add_document(title=pdf_file, content=content, path=pdf_path)

    writer.commit()
