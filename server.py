#!/usr/bin/env python3

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the query parameter
    # Mocked response: Replace with your logic to fetch image URLs
    images = [f"https://example.com/image_{i}.jpg" for i in range(10)]
    return jsonify(images)

if __name__ == '__main__':
    app.run(debug=True)
