# Swarm/ElasticSearch Challenge

## Docker Images

* deploy stack: `docker stack deploy -c docker-compose.yml eventstream`
* check services: `docker service ls`

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