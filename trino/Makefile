run-docker:
	docker run \
	-d \
	--name trino  \
	-p 8080:8080 \
	--volume $PWD/etc/catalog:/etc/trino/catalog \
	trinodb/trino