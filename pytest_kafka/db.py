#!/usr/bin/env python
# coding=utf-8
import copy
import yaml
from pytest_kafka.kafka_client import KafkaClient
from pytest_kafka.logger import logger


def singleton(cls):
    def _singleton(*args, **kwargs):
        instance = cls(*args, **kwargs)
        instance.__call__ = lambda: instance
        return instance

    return _singleton


@singleton
class DB(object):
    def __init__(self, kafkacmdopt, rootdir):
        config_path = '{0}/{1}'.format(rootdir, kafkacmdopt)
        with open(config_path) as f:
            self.env = yaml.load(f, Loader=yaml.FullLoader)

    def __del__(self):
        for k, v in self.kafka.items():
            if k != 'topics':
                self.kafka[k].stop()
                self.kafka[k].c.close()

    @property
    def kafka(self):
        kafka_dict = dict()
        kafka_dict['topics'] = {}
        conf = copy.deepcopy(self.env.get('kafka', {}))
        try:
            for k, v in conf.items():
                v['bootstrap.servers'] = ','.join(v['bootstrap.servers'])
                kafka_dict['topics'].update(v.pop('topics'))
                kafka_dict[k] = KafkaClient(**v)

        except Exception as e:
            logger.error(e)
            raise ConnectionError(e)

        return kafka_dict
