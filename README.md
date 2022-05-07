# Google Cloud Exam Question Analyzer

While studying for [Google's Professional Data Engineer Certification](https://cloud.google.com/certification/data-engineer), I took a number of practice exams.

I wanted a way to find commonalities across the questions I got wrong to identiy areas I needed to study further.

To accomplish this, and to learn a bit more about Google cloud, I created this system to analyze a question.

## Setup

To run this system you need to:

0. You probably want to create a new Google Cloud project
1. Create a BigQuery dataset and table with the schema:

	```json
	 [
	  {
	    "mode": "REQUIRED",
	    "name": "question",
	    "type": "STRING(2000)"
	  },
	  {
	    "mode": "REQUIRED",
	    "name": "keywords",
	    "type": "ARRAY<STRING(100)>"
	  }
	] 
	```

2. Deploy the code in this repo to Cloud Run
  - You can do this by forking the [base repo](https://github.com/fhightower/google-cloud-exam-question-analyzer) and using Cloud Build to trigger builds when a change is pushed (or builds can be triggered on-demand in this way)
3. Add environment variable to Cloud Run app with name `BQ_TABLE_PATH` and value of the path to the BigQuery table and dataset you created in step 1 (it will have the format `{project-id}.{dataset-name}.{table-name}` (example: `bigquery-public-data.usa_names.usa_1910_2013`))
4. Now, you can post questions you got wrong (and I recommend also posting the correct answer) to the system like:

```
curl -X POST -H "Content-Type: application/json" -d '{"question": "..."}' https://CLOUDRUN-DOMAIN-NAME-REPLACE-ME
```

5. Do some analysis in BigQuery:

	You can use this query to view keywords and their counts:

	```sql
	SELECT
	  kws,
	  COUNT(*)
	FROM
	  `{DATABASE-PATH}`,
	  UNNEST(keywords) AS kws
	GROUP BY
	  kws
	```

## Future Work (if this were a production system...)

I'm not going to invest very much time into this project, but if I were I would consider:

1. Designing the system to scale more effectively by:
  - Publish questions and keywords to Pub/Sub rather than writing directly to BigQuery
  - Create a new cloud function to trigger when something is added to Pub/Sub and insert the new data in BigQuery (checking to make sure the question does not already exist - so I'd probably hash each question and store than in BQ too)
2. Consider finding a better way to write data into BQ
  - Avoid using inserts which may not scale well (there's a [quota](https://cloud.google.com/bigquery/quotas#load_job_per_table.long) of 1,500 insert statements a day whereas [batch loads](https://cloud.google.com/bigquery/docs/batch-loading-data) are not subject to the same quota and would work equally well if requirements allowed)
  - Consider storing question/keyword data as [json](https://cloud.google.com/bigquery/docs/reference/standard-sql/json-data)
3. Clean up code
  - The code is hacked together and is not a representation of my best work
  - Add local tests
4. Improve keyword parsing
  - Perhaps consider part of speech more heavily (e.g. find and return all noun phrases)
5. Capture the correct answer

And certainly more...

