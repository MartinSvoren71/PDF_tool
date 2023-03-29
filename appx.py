import textract
import glob

def search_pdf_files(keyword, directory):
    results = []
    for filename in glob.glob(f"{directory}/sample.pdf"):
        text = textract.process(filename).decode("utf-8")
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            if keyword in line:
                results.append((filename, line_num, line))
    return results


results = search_pdf_files("capital", "pdf_files")
for result in results:
    print(result)