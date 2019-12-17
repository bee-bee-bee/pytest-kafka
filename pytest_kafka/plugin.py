# -*- coding: utf-8 -*-
import pytest
from configparser import ConfigParser
from pytest_kafka.db import DB


def pytest_addoption(parser):
    group = parser.getgroup('pytest_kafka')
    group.addoption(
        '--config_kafka',
        action='store',
        # default='config/config.yml',
        help='relative path of config.yml'
    )


@pytest.fixture(scope="session", autouse=False)
def kafkacmdopt(request):
    option_config = request.config.getoption("--config_kafka")
    if option_config:
        return option_config
    else:
        try:
            ini_config = request.config.inifile.strpath
            config = ConfigParser()
            config.read(ini_config)
            kafka_config = config.get('kafka', 'config')
            return kafka_config
        except Exception as e:
            raise RuntimeError("there is no kafka config in pytest.ini", e)


@pytest.fixture(scope="session", autouse=False)
def kafka(kafkacmdopt, request):
    return DB(kafkacmdopt, request.config.rootdir).kafka
