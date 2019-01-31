import os
import socket
from time import strftime
from datetime import datetime
from flask import Flask, request, json, jsonify
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://elasticsearch:9200'])

def xform(event):
    eventType = event['eventType']
    eventValue = event['eventValue']
    with open(f'data/{eventType}.json') as eventFile:
        data = json.load(eventFile)
        id = data[eventValue]
        event['eventId'] = id
    res = es.index(index=eventType, doc_type='event', body=event)
    return res

# web endpoint:
app = Flask(__name__)

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