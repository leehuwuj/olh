

## Deltalake Operator
- The operator for Deltalake which using Delta standalone instead of Spark
- [DEPRECATED]: 
    - Use the `delta-rs` instead of Delta standalone. The delta-rs is an Delta SDK built in Rust which supports us interact with Delta transaction log without Spark. It also has a Python binding version which is easy to use.