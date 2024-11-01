# -------------------------------------导包--------------------------------------
from datetime import datetime

from PIL import Image, ImageSequence
import uuid
import hashlib
import os
import jwt
import re
from flask_app import MESSAGE_DICT
from configs.config import BASE_DIR


# ----------------------------------用户模块--------------------------------------
def time_format(str_time):
    if isinstance(str_time, datetime):
        return str_time
    res = datetime.strptime(str_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return res


def get_token_info(token):
    from flask_app.databases import redis_cache
    res = redis_cache.get(token)
    return res


def validate_params(account=None, passwd=None, email=None,
                    phone=None, gender=None):
    """
    参数校验
    :param account: 账号
    :param passwd: 密码
    :param email: 邮箱
    :param phone: 手机号
    :param gender: 性别
    :return:
    """
    # 校验账号规则
    if account:
        # 账号长度必须为4-20字符
        if not (4 <= len(account) <= 20):
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("账号")
        # 账号只能由数字、字母、下划线组成
        if not re.match(r'^[a-zA-Z0-9_]+$', account):
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("账号")

    # 校验密码规则
    if passwd:
        if len(passwd) < 6:  # 长度不能小于6
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")
        if not any(char.isdigit() for char in passwd):  # 必须有数字
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")
        if not any(char.islower() for char in passwd):  # 必须有小写字母
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")
        if not any(char.isupper() for char in passwd):  # 必须有大写字母
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")

    # 校验邮箱规则
    if email:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                        email):
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("邮箱")

    # 校验手机号规则
    if phone:
        if not re.match(r'^1\d{10}$', phone):  # 必须1开头后面跟10个数字
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("手机号")

    # 校验性别规则
    if gender:
        if gender not in ['男', '女', '保密']:  # 性别必须为'男', '女' 或者 '保密'
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("性别")

    # 可以添加其他复杂度规则
    return MESSAGE_DICT.SUCCESS


def encrypt_pass(passwd):
    """
    密码加密
    :param passwd:
    :return:
    """
    passwd = "".join(chr(ord(char) + 1) for char in passwd)
    hash_algorithm = hashlib.sha256()
    passwd = passwd.encode('utf-8')
    hash_algorithm.update(passwd)
    encrypted_passwd = hash_algorithm.hexdigest()

    return encrypted_passwd


def create_token(account, username, email, phone, profession, member_level):
    """
    :param account: 账号
    :param username: 用户名
    :param email: 邮箱
    :param phone: 手机号
    :param profession: 职业
    :param member_level: 会员等级
    :param class_id: 班级ID
    :return:
    """
    payload = {"account": account,
               'username': username,
               'email': email,
               'phone': phone,
               'profession': profession,
               "member_level": member_level}

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    return token


def page_limit_skip(page=None, limit=None):
    """
    分页查询统一判定, 分页数目和页码
    :param limit:
    :param page:
    :return:
    """
    if not limit or limit == '':
        limit = 10
    else:
        limit = int(limit)
    if not page or page == '':
        page = 1
    skip_d = (int(page) - 1) * int(limit)
    return skip_d, limit


# ----------------------------------上传图片处理----------------------------------
def save_path(module_name):
    path = f'{BASE_DIR}{module_name}/'
    # 确保目标目录存在，如果不存在则创建
    if not os.path.exists(path):
        os.makedirs(path)
    after = f"{uuid.uuid4().hex[:10]}.jpg"
    return f'{module_name}/{after}'


def save_file(module_name, file):
    """
    生成唯一的文件名并保存文件
    :param module_name:模块名，文件保存按模块区分
    :param file:文件
    """
    # 获取文件后缀
    # 生成唯一的文件名
    after_path = save_path(module_name)
    # 保存文件
    compress_and_resize_image(file, 200, 200, after_path)
    return after_path


def compress_and_resize_image(image, width, height, after_path, quality=100,
                              format_='JPEG'):
    """
    压缩并调整图片尺寸
    :param image: 图片
    :param width: 宽
    :param height: 高
    :param after_path: 保存路径
    :param quality: 质量
    :param format_: 类型
    """
    with Image.open(image) as img:
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
        img_resized.save(after_path, format=format_, quality=quality)


def remove_file(path):
    full_path = f"{BASE_DIR}{path}"
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
        return True
    except:
        raise Exception('删除文件失败')


