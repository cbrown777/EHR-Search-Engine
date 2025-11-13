import asyncio
from dotenv import dotenv_values
from elasticsearch import AsyncElasticsearch
import os


# read env variables
working_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(working_dir, '.env')
config = dotenv_values(dotenv_path=dotenv_path)


# set up elasticsearch client
hosts = "https://{}:{}@localhost:9200".format(
    config['ELASTIC_USERNAME'], config['ELASTIC_PASSWORD'])
ca_cert = os.path.join(working_dir, 'ca.crt')
es = AsyncElasticsearch(
  hosts=hosts,
  ca_certs=ca_cert
)


# Query DSL https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
async def search():
    index_name = 'patient_chart'
    query = {
        "match": {
            "PatientID": {
                "query": "150BE8CC-A1B5-49C3-AC56-C0FC7D8CB4BA",
                "operator": "AND"
            }
        }
    }
    charts = await es.search(index=index_name, query=query)
    print(charts.body['hits']['total']['value'])

loop = asyncio.get_event_loop()
loop.run_until_complete(search())
