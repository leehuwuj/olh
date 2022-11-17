build:
	docker build \
		-t olh/hive-metastore \
		-f Dockerfile \
		.

build-amd64:
	docker buildx \
		build --platform linux/amd64 \
		-t olh/hive-metastore \
		-f Dockerfile \
		.
		
build-arm:
	docker buildx \
		build --platform linux/arm64/v8 \
		-t olh/hive-metastore \
		-f Dockerfile \
		.

docker-run:
	docker run \
		-d \
		--name metastore \
		-p 9083:9083 \
		olh/hive-metastore