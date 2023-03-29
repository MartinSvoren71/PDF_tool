from PyPDF4 import PdfFileReader, PdfFileWriter
from flask import Flask, request, render_template

app = Flask(__name__)

# Open the PDF file
pdf = PdfFileReader("sample1.pdf")

# Check if the PDF is encrypted
if pdf.isEncrypted:
    # Try to decrypt the PDF
    pdf.decrypt("")

# Save the decrypted PDF to a new file
with open("Output.pdf", "wb") as f:
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf.getPage(0))
    pdf_writer.write(f)
    
@app.route("/")
def search():
    return render_template("search.html")

@app.route("/results", methods=["POST"])
def results():
    keyword = request.form["keyword"]
    pdf_file = request.form["Output.pdf"]
    results = search_pdf(keyword, pdf_file)
    return render_template("results.html", results=results)

def search_pdf(keyword, pdf_file):
    results = []
    pdf = PdfFileReader(pdf_file)
    for page_num, page in enumerate(pdf.pages):
        text = page.extract_text()
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            if keyword in line:
                results.append((page_num, line_num, line))
    return results


app.run(host='0.0.0.0', port=5000)
