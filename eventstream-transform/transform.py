import os
import socket
import logging
from time import strftime
from datetime import datetime
from flask import Flask, request, json, jsonify
from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://elasticsearch:9200')

app = Flask(__name__)
es = Elasticsearch([ELASTICSEARCH_URL])


# write to a "durable" queue file
def durable_write(event):
    with open("data/durable_queue.json", 'a+') as durable_queue:
        json.dump(event, durable_queue)
        durable_queue.write("\n")
    return event


# write to elasticsearch
def es_write(event):
    try:
        res = es.index(index=event['eventType'], doc_type='event', body=event)
        return res
    except Exception as e:
        logging.error(str(e))
        res = durable_write(event)
        return event


# find event id
def find_event_id(event):
    try:
        eventType = event['eventType']
        eventValue = event['eventValue']
        with open(f'data/{eventType}.json') as eventFile:
            data = json.load(eventFile)
            id = data[eventValue]
            eventId = id
        return eventId
    except Exception as e:
        logging.error(str(e))
        return None


# transform event by loading and parsing eventType file from disk
def xform(event):
    eventId = find_event_id(event)
    res = es_write(event)
    return res


# web endpoint:
@app.route("/", methods=["POST"])
def event_stream():
    try:
        event = request.get_json(force=True)
        data = None

        # transform lists or single object
        if type(event) == list:
            data = list(map(lambda e: xform(e), event))
        else:
            data = xform(event)

        return jsonify(data)
    except Exception as e:
        print(f'{strftime("%I:%M:%S")} - {str(e)}')
        return str(e), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)