import asyncio
# from datetime import datetime
from dotenv import dotenv_values
from elasticsearch import AsyncElasticsearch
import csv
import os
import sys


# read env variables
working_dir = os.path.dirname(__file__)
dotenv_path = os.path.join(working_dir, os.path.pardir, '.env')
config = dotenv_values(dotenv_path=dotenv_path)


# set up elasticsearch client
hosts = "https://{}:{}@localhost:9200".format(
    config['ELASTIC_USERNAME'], config['ELASTIC_PASSWORD'])
ca_cert = os.path.join(working_dir, 'ca.crt')
es = AsyncElasticsearch(
  hosts=hosts,
  ca_certs=ca_cert
)


async def main():
    index_name = 'patient_chart'
    csv.field_size_limit(sys.maxsize)
    with open(os.path.join(working_dir, os.path.pardir, 'charts2.csv')) as f:
        charts = csv.reader(f)
        fields = []
        for chart in charts:
            values = list(map(lambda field: field.strip(), chart))
            if not len(fields):
                fields = values[1:]
                continue
            doc = dict((fields[i], values[i+1]) for i in range(len(fields)))
            await es.index(index=index_name, id=int(values[0]), document=doc)
            print("inserted doc {}".format(values[0]))
    await es.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
