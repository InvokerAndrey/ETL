es:
	docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.2

indices:
	curl -GET http://127.0.0.1:9200/_cat/indices

schema:
	curl -GET http://localhost:9200/movies/_mapping