from typing import List

from google.cloud import bigquery

# this should look like: `bigquery-public-data.usa_names.usa_1910_2013`
# ({}.{})
BQ_TABLE_PATH = ''

# Construct a BigQuery client object.
client = bigquery.Client()

query = """
    SELECT name, SUM(number) as total_people
    FROM `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE state = 'TX'
    GROUP BY name, state
    ORDER BY total_people DESC
    LIMIT 20
"""
query_job = client.query(query)  # Make an API request.

print("The query data:")
for row in query_job:
    # Row values can be accessed by field name or index.
    print("name={}, count={}".format(row[0], row["total_people"]))


def store_results(question: str, salient_words: List[str]):
    pass

