from flask import Flask, request, render_template
import textract
import glob

app = Flask(__name__)

def search_pdf_files(keyword, directory):
    results = []
    for filename in glob.glob(f"{directory}/*.pdf"):
        text = textract.process(filename).decode("utf-8")
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            if keyword in line:
                results.append((filename, line_num, line))
    return results

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        results = search_pdf_files(keyword, "pdf_files")
        return render_template("results.html", keyword=keyword, results=results)
    return render_template("search.html")

t = Thread(target=initialize_ai)
t.start()
app.run(host='0.0.0.0', port=5000)
