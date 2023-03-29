from flask import Flask, render_template, request
import json
from pathlib import Path
from whoosh.qparser import QueryParser
from whoosh.highlight import ContextFragmenter, HtmlFormatter
from whoosh import scoring
from whoosh.index import open_dir

app = Flask(__name__)
pdf_dir = 'pdf_files'
index_path = Path('indexChameleon.json')

# Load the index from indexChameleon.json file
index = open_dir(index_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    parser = QueryParser("content", index.schema)

    with index.searcher(weighting=scoring.TF_IDF()) as searcher:
        parsed_query = parser.parse(query)
        results = searcher.search(parsed_query, limit=10)

        # Highlight the search terms in the results
        formatter = HtmlFormatter(tagname='strong')
        fragmenter = ContextFragmenter(maxchars=200, surround=50, )
        for hit in results:
            content = hit['content']
            content = formatter.highlight_hit(content)
            content = fragmenter.fragment(content)
            hit['content'] = content

        print("Search results:", results)
        return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True)
