from dotenv import dotenv_values
from elasticsearch import AsyncElasticsearch
import os


class SearchEngine:
    def __init__(self):
        # read env variables
        working_dir = os.path.dirname(__file__)
        dotenv_path = os.path.join(working_dir, '.env')
        config = dotenv_values(dotenv_path=dotenv_path)

        # set up elasticsearch client
        hosts = "https://{}:{}@es01:9200".format(
            config['ELASTIC_USERNAME'], config['ELASTIC_PASSWORD'])
        ca_cert = os.path.join(working_dir, 'certs/ca/ca.crt')
        self.es = AsyncElasticsearch(
            hosts=hosts,
            ca_certs=ca_cert
        )

    # Query DSL https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
    async def search(self, query: str):
        index_name = 'patient_chart'
        query = {
            "multi_match": {
                "query": query,
                "fields": [
                    "Id",
                    "Name",
                    "Gender",
                    "Race",
                    "MaritalStatus",
                    "Language",
                    "PovertyRate"
                ],
                "operator": "AND"
            }
        }
        charts = await self.es.search(index=index_name, query=query)
        print("{} results found".format(charts.body['hits']['total']['value']))
        return charts.body['hits']

    # Query DSL https://www.elastic.co/guide/en/elasticsearch/reference/current/full-text-queries.html
    async def search_chart(self, id: str, query: str):
        index_name = 'patient_chart'
        query = {
            "combined_fields": {
                "query": '{} {}'.format(id, query),
                "fields": [
                    "Id",
                    "ChestXrays",
                    "Notes",
                    "CTs",
                    "Ultrasounds",
                    "MRIs"
                ],
                "operator": "AND"
            }
        }
        highlight = {
            "fields": {
                "ChestXrays": {},
                "Notes": {},
                "CTs": {},
                "Ultrasounds": {},
                "MRIs": {}
            }
        }
        charts = await self.es.search(index=index_name, query=query, highlight=highlight)
        print("{} results found".format(charts.body['hits']['total']['value']))
        return charts.body['hits']
