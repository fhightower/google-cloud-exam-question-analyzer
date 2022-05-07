from typing import List
import logging

from google.cloud import language_v1

logging.basicConfig(level=logging.DEBUG)

# I have found the salience to be a relatively bad determiner of what's important in a question so this value is very low
SALIENCE_THRESHOLD = 0.1


def _is_used_as_proper_noun(mentions) -> bool:
    for mention in mentions:
        if language_v1.EntityMention.Type(mention.type_).name == "Proper":
            return True
    return False


def analyze_entities(text_content: str):
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
    
    return salient_entities


