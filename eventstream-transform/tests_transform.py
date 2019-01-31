import os
import tempfile
import json
import pytest
import transform 
import logging


@pytest.fixture
def client():
    transform.app.config['TESTING'] = True
    client = transform.app.test_client()
    yield client


def test_event(client):
    rv = client.post('/', data = """
    {"eventType": "engagement", "eventValue": "scroll"}
    """)
    res = json.loads(rv.data)
    assert res['_index'] == 'engagement' and res['result'] == 'created'


def test_event_batch(client):
    rv = client.post('/', data = """
    [
        {"eventType": "engagement", "eventValue": "scroll"},
        {"eventType": "engagement", "eventValue": "scroll"},
        {"eventType": "engagement", "eventValue": "click"}
    ]
    """)
    batch_res = json.loads(rv.data)
    for res in batch_res:
        assert res['_index'] == 'engagement' and res['result'] == 'created'


def test_find_event_id():
    event = {"eventType": "engagement", "eventValue": "scroll"}
    event_id = transform.find_event_id(event)
    assert event_id == 's'

    event = {"eventType": "engagement", "eventValue": "doubleclick"}
    event_id = transform.find_event_id(event)
    assert event_id is None

    event = {"eventType": "adblock", "eventValue": "doubleclick"}
    event_id = transform.find_event_id(event)
    assert event_id is None

