#!/usr/bin/env python3
import time
import math
import argparse
import sys
import os

import pandas as pd
from flask import Flask, request, jsonify, render_template, send_from_directory

from query import query_index

app = Flask(__name__, template_folder="templates")

@app.route('/search', methods=['GET'])
def search():
    images_per_page = 9

    query = request.args.get('query')  # Get the query parameter
    page = int(request.args.get('page', 0))
    start_time = time.time()
    df = app.do_query(query)  # all results

    df_sel = df.head(images_per_page * (page +1)).tail(images_per_page)
    images = df_sel["image"].values.tolist()
    similarities = df_sel["similarity"].values.tolist()
    end_time = time.time()
    print(images)
    result = {
        "images": images,
        "similarities": similarities,
        "meta": {
            "processing_time": (end_time - start_time),
            "max_pages": math.ceil(len(df) / images_per_page),
            "current_page": page
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


@app.route('/full/<path:path>')
def full_res_imgs(path):
    return send_from_directory('full/', path)


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='clipse web server',
                                     epilog="stg7 2025",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--index_file", type=str, default="./index/test_images.json", help="folder for storing the clipse index")
    a = vars(parser.parse_args())

    assert(os.path.isfile(a["index_file"]))

    app.do_query = query_index(a["index_file"])
    app.run(debug=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

