# Hive standalone metastore
From Hive version 3 design, it is able to deploy the metastore as standalone service. Because we apply the Trino (PrestoSQL) as default query engine so the Hive query engine is not required to include.

The Hive metastore using a RDBMS to store metadata persistantly, by default it's support for MySQL but it's not problem with other DB. We will use the Postgres DB instead.

# Prerequisite
- Postgres: A postgres database to store hive metadata along with its access account
- MinIO Bucket: Specify the warehouse path of managed data. It is optional when initial setup step. Please make sure the s3 credentials of Hive is able to access to external bucket/path as well.

# Setup
## Docker
### 1. Update Hive metastore configuration
Look at the [metastore-site.xml](https://github.com/leehuwuj/olh/blob/main/hive-metastore/metastore-site.xml) file and edit all **[CHANGE_ME]** corresponding to your instance information.  

**Trick**:  If you are testing at your local machine, put the endpoint related to Docker image as `host.docker.internal` along with target service port to easily access the service. Examples:
- MinIO endpoint: `http://host.docker.internal:9000`
- Postgres endpoint: `jdbc:postgresql://host.docker.internal:5432/[DB]`

The `metastore-site.xml` file is located at `${HIVE_HOME}/conf`. Based on your deployment, it can be mounted/replacement for security purpose!

### 2. Build-up the image
From my testing, Hive only supports Java 8, my Dockerfile is inherited from the Azul Java 8 which is compatible to run on my ARM machine (Apple silicon M1 Pro), it'll work well on Intel/AMD also.  

Run the command to build the docker image:
```shell
docker build \
		-t olh/hive-metastore \
		-f Dockerfile \
		.
```
or just simply `Make` it by:   
```shell
make build
```

### 3. Init database schema:
Run a Hive container to init the schema on Postgres:
```shell
docker run \
    --name metastore-init-db \
    olh/hive-metastore \
    init
```

### 4. Start the Hive metastore container:
```shell
docker run \
    --name metastore \
    -p 9083:9083 \
    olh/hive-metastore
```