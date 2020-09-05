import os
from importlib import import_module

from src import exceptions


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    PRODUCTION = False


class ProductionConfig(Config):
    PRODUCTION = True


class DevelopmentConfig(Config):
    ENVIRONMENT = 'development'
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True
    ENVIRONMENT = 'testing'


def get_config() -> Config:
    config_imports = os.environ['APP_SETTINGS'].split('.')
    config_class_name = config_imports[-1]
    config_module = import_module('.'.join(config_imports[:-1]))
    config_class = getattr(config_module, config_class_name, None)
    if not config_class:
        raise exceptions.ConfigClassNotFound('Could not find a config class in {}'.format(os.environ['APP_SETTINGS']))
    return config_class
