## 简介
pytest-kafka插件
## 安装

`pip install pytest-kafka -i http://*:8082/private_repository/ --trusted-host *`

## 使用
### 测试用例可使用kafka fixtrue

```python
def test_kafka(kafka):
    data = kafka['comn'].consume(kafka['topics']['vehicle_data'], timeout=10)
```
### 运行测试
需编写pytest.ini文件，置于项目内的根目录上，用于指定kafka配置路径。
默认在项目内的根目录下寻找环境对应配置(./config/config.yml)

####pytest.ini
```ini
[kafka]
config = config/config.yml
```
或在命令行中通过--config参数指定路径
```bash
pytest --config_kafka config/config.yml
```
####test_config.yml配置如下:
```yaml
kafka:
  comn:
    bootstrap.servers:
      - kafkaip:9092
      - kafkaip:9092
      - kafkaip:9092
      - kafkaip:9092
      - kafkaip:9092
    group.id: ev_monitor_test
    auto.offset.reset: latest
    security.protocol: sasl_plaintext
    sasl.mechanisms: PLAIN
    sasl.username: you_user_name
    sasl.password: *
    enable.partition.eof: False
    topics:
      topic_name1: your_kafka_topic
      topic_name2: your_kafka_topic
      topic_name3: your_kafka_topic
      topic_name4: your_kafka_topic
```
## 打包
`python setup.py sdist bdist`  
`twine upload -r my_nexus dist/*`