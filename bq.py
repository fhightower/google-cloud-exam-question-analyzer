from typing import List
import json
import logging
import os

from google.cloud import bigquery

logging.basicConfig(level=logging.DEBUG)

# this should look like: `bigquery-public-data.usa_names.usa_1910_2013`
# ({project_id}.{dataset}.{table})
BQ_PATH_ENV_VAR_NAME = "BQ_TABLE_PATH"
try:
    BQ_TABLE_PATH = os.environ[BQ_PATH_ENV_VAR_NAME]
except KeyError:
    raise RuntimeError(f"Unable to find the required {BQ_PATH_ENV_VAR_NAME} environment variable.")

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
INSERT
  `{}` (question, keywords)
VALUES
  ("{}", {})
"""


def store_results(question: str, salient_words: List[str]):
    full_query = query.format(BQ_TABLE_PATH, question, json.dumps(salient_words))
    logging.debug(f"Full query: {full_query}")
    query_job = client.query(full_query)  # Make an API request.
    logging.debug(f"Query job: {query_job}")

    print("The query data:")
    for row in query_job:
        # Row values can be accessed by field name or index.
        print("name={}, count={}".format(row[0], row["total_people"]))

