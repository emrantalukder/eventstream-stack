# Swarm/ElasticSearch Challenge

## Usage

* deploy stack: `docker stack deploy -c docker-compose.yml eventstream`
* open browser to `http://localhost:8080`
* click on "Publish" for each specific event
* sent bulk events by pressing "Publish All" for that event type

## Configuration Options

* `docker-compose.yml` contains sensible defaults
* `eventstream-transform` is the transform service that can be scaled using replicas.
* `eventstream-transform` uses the following Environment Variables:
    * `GUNICORN_WORKERS=2`: set the number of workers depending on the num cpus
    * `ELASTICSEARCH_URL=http://elasticsearch2:9200`: used for testing between different elasticsearch services

#### Rational

Click and engagement sometimes come in batched, so I've tried to simulate this behavior using some javascript in the `index.html` found in `eventstream-nginx/www`. AJAX request are sent to the backend server running the `eventstream-transform` flask application.

The `eventstream-transform` python app gets the POST request, checks if it is a batch of events or a single event, reads the json file corresponding to the eventType, extracts the event ID, and finally sends an index request to ElasticSearch.

If the ElasticSearch cluster is not responsive, the event will still be processed but instead of going to elasticsearch (which has timed out), the event will be written to file.

## Docker Images

The included `docker-compose.yml` file uses the images below.

* nginx: `emrantalukder/eventstream-nginx:latest`
* transform service: `emrantalukder/eventstream-transform:latest`
* elasticsearch 6.5.4: `docker.elastic.co/elasticsearch/elasticsearch:6.5.4`
* kibana 6.5.4 (optional): `docker.elastic.co/kibana/kibana:6.5.4`

## Resiliency

Resiliency considerations come in multiple forms. Major concerns are hardware, and software settings. Hardware can be scaled by the size (vertical) and number of nodes (horizontal), while software can be controlled through settings and other configuration.

Here are some ways to add resiliency to the stack:

* Add durability to the Transform service in case ElasticSearch goes down.
* Add more master nodes, data nodes and failover nodes for ElasticSearch
* Keep backups of the elasticSearch data since reindexing can be done quickly.
* Increase the number of replicas to improve read performance and redundancy.
* Do not let a single index get too large, or increase the number of shards.
* Consider adding a time-based indexing pattern, such that no index grows too large, latest data can be loaded first for your users, and retention policies are easier to enforce.
* Scale the Transform service with more Swarm replicas. UI events will be load balanced.
* The Transform service will bottleneck due to i/o for reading the JSON files to determine the event ID. Consider using an in-memory heap or in-memory filesystem to keep this data if it changes often such as Alluxio or Apache Ignite.
* Consider using ElasticSearch's Bulk API, batching techniques, timing or throttling the stream to N messages per second.

## Testing

* Code was tested locally 
* Services were tested by downing them one at a time, and making sure exceptions were handled appropriately.
* Unit tests are provided in `eventstream-transform/test_transform.py`
    * run using `pytest eventstream-transform/test_transform.py`
    * more tests are needed for the ES failure, write to disk (durable_queue function test)