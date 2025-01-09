#!/usr/bin/env python3
import time

import pandas as pd
from flask import Flask, request, jsonify, render_template, send_from_directory

from query import query_index

app = Flask(__name__, template_folder="templates")

do_query = query_index("./index/photos.json")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the query parameter
    # Mocked response: Replace with your logic to fetch image URLs
    start_time = time.time()
    df = do_query(query)
    images = df.head(10)["image"].values.tolist()
    end_time = time.time()
    print(images)
    result = {
        "images": images,
        "meta": {
            "processing_time": (end_time - start_time)
        }
    }
    return jsonify(result)


@app.route('/')
def index():
    return render_template('search.html')


@app.route('/photos/<path:path>')
def imgs(path):
    # Using request args for path will expose you to directory traversal attacks
    return send_from_directory('photos', path)


@app.route('/full/photos/<path:path>')
def full_res_imgs(path):
    return send_from_directory('full/photos', path)


if __name__ == '__main__':
    app.run(debug=True)
