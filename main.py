import os
import logging
from typing import List

from flask import Flask, request, jsonify
from google.cloud import language_v1

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
# I have found the salience to be a relatively bad determiner of what's important in a question so this value is very low
SALIENCE_THRESHOLD = 0.1


def _is_used_as_proper_noun(mentions) -> bool:
    for mention in mentions:
        if language_v1.EntityMention.Type(mention.type_).name == "Proper":
            return True
    return False


def sample_analyze_entities(text_content: str):
    """ Analyzing Entities in a String

    Args: text_content The text content to analyze """
    salient_entities: List[str] = []
    client = language_v1.LanguageServiceClient()

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})
    for metadata_name, metadata_value in entity.metadata.items():
            logging.info(u"{}: {}".format(metadata_name, metadata_value))

    # Loop through entitites returned from the API
    for entity in response.entities:
        if entity.salience > SALIENCE_THRESHOLD:
            salient_entities.append(entity.name)
        # keep entities w/ metadata as they are likely important regardless of salience
        elif 'mid' in entity.metadata or 'wikipedia' in entity.metadata:
            salient_entities.append(entity.name)
        # keep entities which are proper nouns
        elif _is_used_as_proper_noun(entity.mentions):
            salient_entities.append(entity.name)

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    logging.info(u"Language of the text: {}".format(response.language))
    
    return salient_entitiy_names


@app.route("/", methods=['GET','POST'])
def hello_world():
    data = request.get_json()
    question = data['question']
    results = sample_analyze_entities(question)
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

