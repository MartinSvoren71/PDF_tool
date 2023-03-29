import textract
import glob

def search_pdf_files(keyword, directory):
    results = []
    for filename in glob.glob(f"{directory}/*.pdf"):
        text = textract.process(filename).decode("utf-8")
        lines = text.split("\n")
        for line_num, line in enumerate(lines):
            if keyword in line:
                results.append((filename, line_num, line))
    return results

results = search_pdf_files("temperature", "/")
for result in results:
    print(f"{result[0]}, line {result[1]}: {result[2]}")
