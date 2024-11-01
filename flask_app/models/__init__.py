# -*- coding: UTF-8 -*-
import time

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
            if kwargs.get("entities"):
                # 是否返回指定列
                entities = kwargs.pop('entities')
            if kwargs.get("sort"):
                # 是否排序
                sort = kwargs.pop('sort')
            if kwargs.get('is_one'):
                # 是否查询匹配条件的第一个元素
                is_one = kwargs.pop('is_one')
            res = cls.query.with_entities(*entities).filter(*args).filter_by(
                **kwargs)
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
            logging.warning(f'sql find one error: {e}')
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
        res = cls._find(is_one=True, *args, **kwargs)
        return res.to_dict() if res else {}

    @classmethod
    def update_by_id(cls, id_, update_json, sort=None):
        """
        通过id更新信息
        :param id_:
        :param update_json:
        :param sort:
        :return:
        """
        res = cls._find(id=id_, sort=sort, is_one=True)
        if res:
            res.update_data(update_json)
            return res.to_dict()

    @classmethod
    def find_all(cls, entities=None, sort=None, *args, **kwargs):
        translate = kwargs.pop('translate', True)
        res = cls._find(entities=entities, sort=sort, *args, **kwargs)
        return [i.to_dict() for i in res] if translate else res

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
        _id = self.id
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
