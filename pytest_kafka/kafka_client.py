#!/usr/bin/env python
# coding=utf-8

import time

from confluent_kafka.cimpl import Consumer, Producer, TopicPartition
try:
    from pytest_kafka.logger import logger
except Exception:
    import logging
    logger = logging.getLogger(__name__)


class KafkaClient(object):
    def __init__(self, **kwargs):
        self.c = Consumer(**kwargs)
        self.p = Producer(**kwargs)
        self.loop = True

    def consume(self, topics, timeout=None):
        """

        :param topics: need to consumed kafka topic
        :param timeout: consume wait second
        :return:
        """
        self.c.subscribe([topics])

        if timeout is None:
            while self.loop:
                msg = self.c.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.debug("Consumer error: {}".format(msg.error()))
                    continue
                # logger.debug('===={} {}'.format(msg.partition(), msg.offset()))
                yield msg.value()
        elif isinstance(timeout, int):
            deadline = time.time() + timeout
            while time.time() < deadline:
                # poll every second to consume messages
                msg = self.c.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    logger.debug("Consumer error: {}".format(msg.error()))
                    continue
                # logger.debug('===={} {}'.format(msg.partition(), msg.offset()))
                yield msg.value()

        else:
            logger.error('Consume error')



    def stop(self):
        self.loop = False

    def produce(self, topic, value):
        self.p.produce(topic, value, callback=self.send_callback)
        self.p.poll(0)
        self.p.flush()

    @staticmethod
    def send_callback(err, msg):
        if err:
            logger.error("Fail:send fail cause:{0}".format(err))
        else:
            logger.debug("Successfully send to [{}], Data is:\n {}".format(msg.topic(), msg.value()))


    def set_offset_to_end(self, topic):
        self.c.subscribe([topic])

        # 循环poll，直到可以得到topic的partition信息
        while not self.c.assignment():
            msg = self.c.poll(1.0)
            self.c.commit()

        for index, topic_partition in enumerate(self.c.assignment()):
            # 获取offset最大最小值
            watermark_offsets = self.c.get_watermark_offsets(topic_partition)
            logger.debug('watermark_offsets {}'.format(watermark_offsets))

            # 直接将offset置为logsize,跳过未消费的数据
            logsize = watermark_offsets[1]
            tp_new = TopicPartition(topic, index, int(logsize))
            self.c.commit(offsets=[tp_new], async=False)
