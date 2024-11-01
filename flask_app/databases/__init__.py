# -------------------------------------导包--------------------------------------
import logging
import pickle
from configs.config import current_config, rd
from configs.application import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# -------------------------------------mysql--------------------------------------
engine = create_engine(current_config.SQLALCHEMY_DATABASE_URI)
app.config.from_object(current_config)

# -------------------------------------redis--------------------------------------
class RedisManager(object):
    _redis_conn = rd

    @property
    def redis_conn(self):
        if not self._redis_conn:
            self._redis_conn = rd
        return self._redis_conn

    def get(self, key):
        try:
            # 通过key查询redis的值
            res = self.redis_conn.get(key)
            if res:
                try:
                    # 反序列化
                    return pickle.loads(res)
                except:
                    # 解码
                    return res.decode('utf-8')
        except Exception as e:
            logging.error(f"Redis查询失败， 报错提示为{e}", exc_info=False)
            return None

    def set(self, key, value, ex_time=60):
        try:
            self.redis_conn.set(key, value, ex=ex_time)
            return True
        except Exception as e:
            logging.error(f"Redis操作失败， 报错提示为{e}", exc_info=False)
            return False

    def inc(self, key, ex_time=60):
        res = self.get(key)
        if res:
            try:
                self.redis_conn.incr(key)
            except Exception as e:
                logging.error(f"Redis自增失败， 报错提示为{e}", exc_info=False)
                raise Exception('Redis自增失败')
        else:
            if not self.set(key, 1, ex_time):
                raise Exception('Redis自增失败')
        return True

    def delete(self, key):
        res = self.get(key)
        if res:
            try:
                self.redis_conn.delete(key)
            except Exception as e:
                logging.error(f"Redis删除失败， 报错提示为{e}", exc_info=False)
                raise Exception('Redis删除失败')
        else:
            return True


# ------------------------------------单例-------------------------------------
db = SQLAlchemy(app=app, session_options={"expire_on_commit": False})
redis_cache = RedisManager()
