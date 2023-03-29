from flask import Flask, request, render_template
import glob
from pdfminer.high_level import extract_text

app = Flask(__name__)

@app.route("/")
def search():
    return render_template("search.html")

@app.route("/results", methods=["POST"])
def results():
    keyword = request.form["keyword"]
    directory = request.form["directory"]
    results = search_pdf_files(keyword, directory)
    return render_template("result.html", results=results)

def search_pdf_files(keyword, directory):
    results = []
    for filename in glob.glob(f"{directory}/sample.pdf"):
        text = extract_text(filename)
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            if keyword in line:
                results.append((filename, line_num, line))
    return results


app.run(host='0.0.0.0', port=5000)
