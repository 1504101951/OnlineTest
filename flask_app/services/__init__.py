# -------------------------------------导包--------------------------------------
import logging
import traceback
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
    res = redis_cache.get(f"token:{token}")
    return res


def validate_params(account=None, password=None, email=None,
                    phone=None, gender=None):
    """
    参数校验
    :param account: 账号
    :param password: 密码
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
    if password:
        if len(password) < 6:  # 长度不能小于6
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")
        if not any(char.isdigit() for char in password):  # 必须有数字
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")
        if not any(char.islower() for char in password):  # 必须有小写字母
            return MESSAGE_DICT.PARAMS_NOT_VALID.format("密码")
        if not any(char.isupper() for char in password):  # 必须有大写字母
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


def encrypt_pass(password):
    """
    密码加密
    :param password:
    :return:
    """
    password = "".join(chr(ord(char) + 1) for char in password)
    hash_algorithm = hashlib.sha256()
    password = password.encode('utf-8')
    hash_algorithm.update(password)
    encrypted_passwd = hash_algorithm.hexdigest()

    return encrypted_passwd


def check_pass(password, check_passwd):

    # 判断两次密码输入是否一致
    if password != check_passwd:
        return {"message": MESSAGE_DICT.CHECK_PASSWD_ERROR}

    # 判断密码是否合规
    check_param = validate_params(password=password)
    if check_param != MESSAGE_DICT.SUCCESS:
        return {"message": check_param}

    # 密码加密
    password = encrypt_pass(password)
    return {'message': MESSAGE_DICT.SUCCESS, 'password': password}


def create_token(account, username, email, phone, introduce, profession, image,
                 member_level=0, is_admin=False):
    """
    :param account: 账号
    :param username: 用户名
    :param email: 邮箱
    :param phone: 手机号
    :param profession: 职业
    :param introduce: 自我介绍
    :param image: 头像
    :param member_level: 会员等级
    :param is_admin: 是否为管理员
    :return:
    """
    payload = {"account": account,
               'username': username,
               'email': email,
               'phone': phone,
               "image": image,
               'profession': profession,
               "introduce": introduce,
               "member_level": member_level,
               "is_admin": is_admin}

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
def save_file(module_name, file):
    """
    生成唯一的文件名并保存文件
    :param module_name:模块名，文件保存按模块区分
    :param file:文件
    """
    # 获取文件后缀
    # 生成唯一的文件名
    after = f"{uuid.uuid4().hex[:10]}.jpg"
    path = f'{BASE_DIR}{module_name}'
    # 确保目标目录存在，如果不存在则创建
    if not os.path.exists(path):
        os.makedirs(path)
    if compress_and_resize_image(file, 200, 200, f"{path}/{after}"):
        # 保存文件
        return {"image": after, "message": MESSAGE_DICT.SUCCESS}
    return {"image": None, "message": MESSAGE_DICT.OPERATION_FAIL.format("上传")}


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
    try:
        with Image.open(image) as img:
            img_resized = img.resize((width, height), Image.Resampling.LANCZOS)
            img_resized.save(after_path, format=format_, quality=quality)
            return True
    except:
        return False


def remove_file(path):
    full_path = f"{BASE_DIR}{path}"
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
        return True
    except:
        raise Exception('删除文件失败')


def move_file(old_path, new_path):
    try:
        os.rename(f"{BASE_DIR}{old_path}", f"{BASE_DIR}{new_path}")
        return new_path
    except Exception as e:
        logging.error(traceback.format_exc())
        return {"message": MESSAGE_DICT.FILE_UPLOAD_ERROR}

