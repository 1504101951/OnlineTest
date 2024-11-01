# encoding=utf-8

from flask_app.models import BaseModel
from flask_app.databases import db
from sqlalchemy import func, ForeignKey


class User(BaseModel, db.Model):
    __tablename__ = "users"
    account = db.Column(db.String(30), primary_key=True, unique=True, comment='账号')
    username = db.Column(db.String(30), unique=True, comment='用户名')
    password = db.Column(db.String(255), comment='密码', nullable=False)
    sex = db.Column(db.Integer, comment='性别', index=True, nullable=False)
    image = db.Column(db.String(30), comment='头像')
    email = db.Column(db.String(30), unique=True, comment='邮箱', nullable=False)
    phone = db.Column(db.String(20), unique=True, comment='电话', nullable=False)
    introduce = db.Column(db.String(50), comment='自我介绍')
    profession = db.Column(db.String(30), comment='职业', nullable=False)
    is_delete = db.Column(db.Boolean, default=False, comment='是否删除', nullable=False)
    member_level = db.Column(db.Integer, default=False, comment='是否会员', nullable=False)
    create_time = db.Column(db.DateTime, default=func.now(), nullable=False, comment='创建时间')
    update_time = db.Column(db.DateTime, default=func.now(), onupdate=func.now(),
                            nullable=False, comment='更新时间')

    # __table_args__ = (db.Index("idx_sex", "sex"),)


class Token(BaseModel, db.Model):
    __tablename__ = "token"
    account = db.Column(db.String(30), ForeignKey('users.account'), primary_key=True, comment='账号')
    token = db.Column(db.String, comment="token")
