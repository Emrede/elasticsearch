# elasticsearch

### Kibana URL: localhost:5601
### Elasticsearch URL: localhost:9200


To start the application:\
`docker-compose up`

To start the application in detached mode:\
`docker-compose up -d`

To terminate app and destroy everything:\
`docker-compose down`

To check real time logs:\
`docker-compose logs -f consumer producer`

## To see the entries on Kibana interface
 - Go to the Kibana URL from browser
 - Select Discover from Analytics menu 
 - Create an index pattern
 - Enter "test-index" as Name box and select "timestamp" for Timestamp field
 - Now entries should be listed on Discover page
