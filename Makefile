es:
	docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.2

indices:
	curl -GET http://127.0.0.1:9200/_cat/indices

schema:
	curl -GET http://localhost:9200/movies/_mapping

view:
	curl -GET http://localhost:9200/movies/_search?pretty

delete:
	curl -XDELETE localhost:9200/movies/

postgres:
	psql -h localhost -p 5432 -U postgres -W