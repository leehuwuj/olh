# Trino query engine

# Prerequisite
- [Hive metastore](https://github.com/leehuwuj/olh/blob/main/hive-metastore)
- MinIO Bucket: Specify the warehouse path of managed data. It is optional when initial setup step. Please make sure the s3 credentials which Trino is able to access to and the external bucket/path as well.

# Setup
## Docker
### 1. Update Trino catalog config for Hive metastore
Look at the [hive.properties](https://github.com/leehuwuj/olh/blob/main/trino/etc/catalog/hive.properties) file and edit all **[CHANGE_ME]** corresponding to your instance information.  

**Tricks**: 
- If you are testing at your local machine, put the endpoint related to Docker image as `host.docker.internal` along with target service port to easily access the service. Examples:
    - MinIO endpoint: `http://host.docker.internal:9000`
    - Hive thrift server endpoint: `thrift://host.docker.internal:9083`

- You can point out config value to a environment variable by using this syntax: `${ENV:VARIABLE_NAME}`. Example:  
```hive.s3.aws-secret-key=${ENV:AWS_SECRET}```

### 2. Build-up the image
We will reuse the original docker image of Trino.
```
docker pull trinodb/trino
```

### 3. Start trino in Docker container:
- Mount the above catalog config file only:
```shell
docker run \
    -d \
    --name trino  \
    -p 8080:8080 \
    --volume $PWD/etc/catalog:/etc/trino/catalog \
    trinodb/trino
```

# Access
Trino support many kinds of authentication (password, oauth2, kerberos,...) but we will not cover the security in this project scope.
By default, you can access to all trino resource.

## JDBC:
- As other JDBC drivers, you have to download the Trino JDBC driver, add to client application and using trino connection uri.
    - JDBC driver download: https://repo1.maven.org/maven2/io/trino/trino-jdbc/
    - Connection uri:
        ```
        jdbc:trino://<username>:<password>@<host>:<port>/<catalog>/<schema>
        ```
*Trick*: DBeaver is a database tool supports many kind of databases through JDBC. You can easily connect to Trino via DBeaver in your local machine.

## Python client:
- Github source code: https://github.com/trinodb/trino-python-client