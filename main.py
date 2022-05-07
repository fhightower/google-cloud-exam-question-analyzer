import os
import logging

from flask import Flask, request, jsonify

from bq import store_results
from language import analyze_entities

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=['GET','POST'])
def hello_world():
    data = request.get_json()
    question = data['question']
    results = analyze_entities(question)
    store_results(question, results)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

