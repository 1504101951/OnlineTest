# -*- coding: utf-8 -*-
import os

import redis
from urllib.parse import quote_plus
import yaml

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_file = os.path.join(root_path, "config.yaml")
env_config = yaml.load(open(config_file, encoding='utf-8'), Loader=yaml.SafeLoader)
BASE_DIR = f"{root_path}/front/vue-project/src/assets/img/"


# ------------------------------------class-------------------------------------
class Config(object):
    """ 基础配置 """
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 连接池最大连接数
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 连接数可以超过多少个
    SQLALCHEMY_MAX_OVERFLOW = 30
    # 空闲连接回收间隔时间
    SQLALCHEMY_POOL_RECYCLE = 30
    # 连接池的连接超时时间
    SQLALCHEMY_POOL_TIMEOUT = 60
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True, 'pool_use_lifo': True}
    # 打印sql
    SQLALCHEMY_ECHO = False

    CACHE_TYPE = 'redis'

    def __init__(self):
        self.__dict__ = dict(self.__dict__, **env_config)
        self._config()
        self.__config()

    def _config(self):
        # 'mysql+pymysql://{username}:{password}@{host}:{port}/{database}'
        self.SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(
            self.mysql['username'], quote_plus(self.mysql['password']),
            self.mysql['host'],
            self.mysql['port'], self.mysql['database'])

        self.SQLALCHEMY_POOL_SIZE = int(os.environ.get("SQLALCHEMY_POOL_SIZE", self.SQLALCHEMY_POOL_SIZE))
        self.ThreadPoolSize = int(os.environ.get("THREAD_POOL_SIZE", self.SQLALCHEMY_POOL_SIZE))

        self.log_level = int(os.environ.get("LOG_LEVEL", self.log_level))
        # 是否存储log日志（0：不存储 1 存储）
        self.log_save = int(os.environ.get("LOG_SAVE", 0))
        # 是否存储kafka告警全量日志（0：不存储 1 存储）
        self.log_all_save = int(os.environ.get("LOG_ALL_SAVE", 0))

        self.REDIS_CONN_STRING = 'redis://:{}@{}:{}'.format(
            self.redis['password'], self.redis['host'], self.redis['port'])

    def __config(self):
        pass


current_config = Config()
rd = redis.StrictRedis(host=current_config.redis['host'],
                       port=current_config.redis['port'],
                       password=current_config.redis['password'],
                       socket_keepalive=True,
                       retry_on_timeout=True)
