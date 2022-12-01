# Jupyter
- Source: https://github.com/jupyter/docker-stacks/tree/main/pyspark-notebook

## Docker setup
1. Build jupyter spark image:
- This Docker file is inherited from above source
- Added additional dependencies for metastore, delta and s3 integration.
```shell
docker build -t olh/jupyter:base -f Dockerfile .
```

2. Run integration test to Hive metastore:
- Start your Hive metastore instance, update the uri in test file if needed.
- Run test in container:
```shell
docker run --rm -p 10000:8888 olh/jupyter:base /tmp/tests/test.sh
```

Output:
```
============================= test session starts ==============================
platform linux -- Python 3.10.8, pytest-7.2.0, pluggy-1.0.0
rootdir: /tmp/tests
plugins: anyio-3.6.2
collected 1 item

../../tmp/tests/notebook-tester.py . 
========================= 1 passed, 1 warning in 7.89s =========================
```



//Todo: Jupyter lab server  
//Todo: Jupyter- Spark kubernetes integration

