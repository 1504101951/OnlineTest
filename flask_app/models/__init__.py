# -*- coding: UTF-8 -*-
import time
import traceback

import sqlalchemy
import logging
from sqlalchemy import desc, asc, inspect
from sqlalchemy.dialects.postgresql import insert

from flask_app.databases import db


class DataBaseCommitError(Exception):
    def __init__(self, *args, **kwargs):
        super(DataBaseCommitError, self).__init__(*args, **kwargs)  # 调用父类的方法


class BaseModel(object):
    __undict__ = []

    @classmethod
    def create(cls, **kwargs):
        ret = cls()
        for k, v in kwargs.items():
            if k != 'id':
                setattr(ret, k, v)
        db.session.add(ret)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DataBaseCommitError(400, f'数据库提交错误，{str(e)}')
        finally:
            db.session.close()
        return ret

    def update_data(self, data):
        for k in data:
            if k != 'id':
                setattr(self, k, data[k])
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DataBaseCommitError(400, f'数据库提交错误，{str(e)}')
        finally:
            db.session.close()

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            db.session.close()
        except Exception as e:
            db.session.rollback()
            raise DataBaseCommitError(f'数据库删除错误, {str(e)}')

    @classmethod
    def _find(cls, *args, **kwargs):
        res = None
        try:
            entities = [cls]
            sort = None
            is_one = False
            for key, value in kwargs.copy().items():
                match key:
                    case 'sort':
                        sort = kwargs.pop('sort')
                    case 'entities':
                        entities = [getattr(cls, col) for col in kwargs.pop('entities')]
                    case 'is_one':
                        is_one = kwargs.pop('is_one')
            res = cls.query.with_entities(*entities).filter(*args).filter_by(**kwargs)
            sequence_map = {1: asc, -1: desc}
            if sort:
                sort = [sequence_map[int(sequence)](cls.__dict__.get(sort_key))
                        for sort_key, sequence in sort.items()]
                res = res.order_by(*sort)

            if is_one:
                res = res.first()
            else:
                res = res.all()
        except Exception as e:
            logging.error(traceback.format_exc())
            db.session.rollback()
        finally:
            db.session.close()

        return res

    @classmethod
    def find_one(cls, *args, **kwargs):
        """
        查找匹配条件的第一个元素
        :param args:
        :param kwargs:
        :return:
        """
        result = cls._find(is_one=True, *args, **kwargs)
        try:
            result = result.to_dict() if result else {}
        except:
            result = result._asdict() if result else {}
        return result

    @classmethod
    def update(cls, *args, **kwargs):
        """
        通过id更新信息
        :param args:
        :param kwargs:
        :return:
        """
        try:
            update_json = kwargs.pop('update_json')
        except:
            raise ValueError('update_json is required.')
        res = cls._find(is_one=True, *args, **kwargs)
        if res:
            res.update_data(update_json)
            return res

    @classmethod
    def find_all(cls, *args, **kwargs):
        result = cls._find(*args, **kwargs)
        data = []
        for i in result:
            try:
                data.append(i.to_dict())
            except:
                data.append(i._asdict())
        return data

    # @classmethod
    # def get_data_by_filters(cls, _filters, _query=None):
    #     if _query is None:
    #         _query = {}
    #     res = cls.query.filter(*_filters).filter_by(**_query).all()
    #     db.session.close()
    #     return [_.to_dict() for _ in res]
    #
    # @classmethod
    # def get_data_count_by_filters(cls, _filters, _query=None):
    #     if _query is None:
    #         _query = {}
    #     count = cls.query.filter(*_filters).filter_by(**_query).count()
    #     db.session.close()
    #     return count

    def save_session(self):
        db.session.add(self)

    @classmethod
    def save2db(cls):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise DataBaseCommitError(400,
                                      f'数据库提交错误，请检查是否填写完整,{str(e)}')
        finally:
            db.session.close()

    @classmethod
    def remove_by_keys(cls, param):
        res = cls.query.filter_by(**param).delete()
        cls.save2db()
        return res

    @classmethod
    def delete_by_ids(cls, ids):
        """
        批量软删除
        """
        res = cls._find_all(cls.id.in_(ids))
        for i in res:
            i.is_delete = 1
            i.save_session()
        cls.save2db()
        return res

    @classmethod
    def conflict_do_update(cls, data, update_data=None, where_condition=None):
        """新增，失败则更新"""

        mapper = inspect(cls)
        # 筛选出字典中存在于表中的键值对
        insert_data = {key: value for key, value in data.items() if
                       key in mapper.columns}

        if not update_data:
            update_data = insert_data

        merge_stmt = insert(cls).values(**insert_data).on_conflict_do_update(
            index_elements=['alarm_start_time', 'serial_no', 'gateway_id',
                            'gateway_point_id', 'gateway_device_id'],
            set_=update_data,
            where=where_condition
        )
        db.session.execute(merge_stmt)
        cls.save2db()

    def to_dict(self):
        # 读一下id属性，从而确保所有属性正确读入(载入)
        data_properties = {k: v for k, v in list(self.__dict__.items()) if
                           k not in self.__undict__ and not isinstance(
                               v, sqlalchemy.orm.state.InstanceState
                           )}

        data_properties.update(
            {k: getattr(self, k) for k, f in
             list(self.__class__.__dict__.items())
             if (k not in self.__undict__) and isinstance(f, property)
             })
        return data_properties
