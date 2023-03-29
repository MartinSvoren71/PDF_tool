import os
import re
from flask import Flask, render_template, request
from PyPDF4 import PdfFileReader

app = Flask(__name__)

def search_pdf_files(keyword, directory):
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'rb') as pdf_file:
                        pdf_reader = PdfFileReader(pdf_file)
                        if pdf_reader.isEncrypted:
                            print(f"Skipping encrypted file: {filepath}")
                            continue
                        for page_num in range(pdf_reader.getNumPages()):
                            text = pdf_reader.getPage(page_num).extractText()
                            pattern = re.compile(r'(?<=\.)([^.]*\b{}\b[^.]*(?:\.[^.]*){{0,1}})'.format(keyword))
                            matches = pattern.findall(text)
                            if matches:
                                if filepath not in results:
                                    results[filepath] = []
                                results[filepath].extend([(page_num, match) for match in matches])
                except Exception as e:
                    print(f"Error processing {filepath}: {str(e)}")
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = {}
    if request.method == 'POST':
        keyword = request.form['keyword']
        directory = "/"  # Replace with the specific directory you want to search
        search_results = search_pdf_files(keyword, directory)
    return render_template('index.html', results=search_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
