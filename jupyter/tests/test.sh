#!/bin/bash
export PYTHONPATH=/usr/local/spark/python/lib/py4j-0.10.9.5-src.zip:/usr/local/spark/python
/opt/conda/bin/python -m pytest /tmp/tests/notebook-tester.py