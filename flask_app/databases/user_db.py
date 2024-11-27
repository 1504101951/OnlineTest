# -------------------------------------导包--------------------------------------
from flask_app.databases import redis_cache
from flask_app import MESSAGE_DICT
from flask_app.models.user_model import User, Token
import pickle

# ------------------------------------静态配置-----------------------------------
token_lives = 60 * 60 * 24 * 7
login_limit_time = 60 * 15


# -----------------------------------内部调用方法---------------------------------
def check_duplicate(account, email, phone, username):
    errors = []
    # 检查账号是否重复
    if User.find_one(account=account, is_delete=False):
        errors.append("账号已存在")

    # 检查邮箱是否重复
    if User.find_one(email=email, is_delete=False):
        errors.append("邮箱已注册")

    # 检查手机号是否重复
    if User.find_one(phone=phone, is_delete=False):
        errors.append("手机号已注册")

    # 检查用户名是否重复
    if User.find_one(username=username, is_delete=False):
        errors.append("用户名已存在")

    # 根据检测结果返回
    if errors:
        return {"message": errors}
    else:
        return {"message": MESSAGE_DICT.SUCCESS}


def check_modify_duplicate(account, email, phone, username):
    """
    检查用户新修改的信息是否有重复
    :param account:
    :param email:
    :param phone:
    :param username:
    :return:
    """
    errors = []
    filter_query = [User.account != account]
    # 检查邮箱是否重复
    if User.find_one(*filter_query, email=email, is_delete=False):
        errors.append("邮箱已注册")

    # 检查手机号是否重复
    if User.find_one(*filter_query, phone=phone, is_delete=False):
        errors.append("手机号已注册")

    # 检查用户名是否重复
    if User.find_one(*filter_query, username=username, is_delete=False):
        errors.append("用户名已存在")
    # 根据检测结果返回
    if errors:
        return {"message": errors}
    else:
        return {"message": MESSAGE_DICT.SUCCESS}


# -----------------------------------接口调用方法---------------------------------
def login(account, password, addr):
    """
    登录
    :param account: 用户名
    :param password: 密码
    :param addr: 发起请求方的地址
    :return:
    """
    # 如果在15分钟内连续五次登录失败则禁止登录
    if redis_cache.get(f"addr:{addr}") not in [None, '1', '2', '3', '4', '5']:
        return {"message": MESSAGE_DICT.LOGIN_LIMIT}
    # 找数据库中匹配账号密码的用户
    entities = ['account', 'username', 'image', 'email', 'phone',
                'introduce', 'profession', 'sex', 'member_level', 'is_admin']
    result = User.find_one(entities=entities, account=account, password=password, is_delete=False)
    # 找不到则视为(账号/密码)错误
    if not result:
        # 在redis中自增1， 防止同一个IP短时间内登录次数过多
        redis_cache.inc(f"addr:{addr}", login_limit_time)
        return {"message": MESSAGE_DICT.LOGIN_ERROR}
    # 从数据库中获取token， 存放到redis中， 并设置过期时间为7天
    token = Token.find_one(account=account)['token']

    # 如果token设置失败, 则视为登录失败, 序列化value
    if not redis_cache.set(f"token:{token}", pickle.dumps(result), ex_time=token_lives):
        return {"message": MESSAGE_DICT.LOGIN_ERROR}
    # redis删除登录失败次数
    redis_cache.delete(f"addr:{addr}")
    # 成功， 返回提示信息与token
    return {"message": MESSAGE_DICT.SUCCESS, "token": token, 'result': result}


def get_user_info(account):
    """
    获取用户信息
    :param account:
    :return:
    """
    entities = ['account', 'username', 'image', 'email', 'phone',
                'introduce', 'profession', 'sex', 'member_level', 'is_admin']
    result = User.find_all(account=account, entities=entities, is_delete=False)
    if not result:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("用户信息")}
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result}


def register(account, username, password, sex, image, phone, email,
             introduce, profession, is_admin, token):
    """
    注册
    :param account: 账号
    :param username: 用户名
    :param password: 密码
    :param sex: 性别
    :param image: 头像
    :param email: 邮箱
    :param phone: 手机号
    :param introduce:: 简介
    :param profession: 用户职业
    :param is_admin: 是否为管理员
    :param token: 用户密钥
    :return:
    """
    is_exist = check_duplicate(account, email, phone, username)
    if is_exist['message'] != MESSAGE_DICT.SUCCESS:
        return {"message": MESSAGE_DICT.REPEAT.format(",".join(is_exist['message']))}

    # 创建用户
    if User.create(account=account, username=username, password=password,
                   sex=sex, image=image, phone=phone, email=email,
                   introduce=introduce, profession=profession, is_admin=is_admin):
        if Token.create(account=account, token=token):
            return {"message": MESSAGE_DICT.SUCCESS}
    # 如果创建失败则返回报错信息
    return {"message": MESSAGE_DICT.OPERATION_FAIL.format("注册")}


def modify_pass(account, old_pass, password, token):
    """
    修改密码
    :param account: 账号
    :param old_pass: 旧密码
    :param password: 新密码
    :param token: 用户密钥
    :return:
    """
    # 如果旧密码与数据库密码不符，则提示旧密码错误
    is_valid = User.find_one(account=account, password=old_pass, is_delete=False)
    if old_pass != is_valid['password']:
        return {"message": MESSAGE_DICT.OLD_PASS_ERROR}

    # 如果新密码与旧密码相同，直接返回成功
    if old_pass == password:
        return {"message": MESSAGE_DICT.SUCCESS}

    if User.update(account=account, update_json={"password": password}):
        redis_cache.delete(f"token:{token}")
        return {'message': MESSAGE_DICT.SUCCESS}

    return {"message": MESSAGE_DICT.OPERATION_FAIL.format('修改密码')}


def modify_info(account, username, email, phone, introduce, profession, image,
                member_level, new_token):
    """
    修改账号信息
    :param account:
    :param username:
    :param image:
    :param email:
    :param phone:
    :param profession:
    :param introduce:
    :param member_level:
    :param new_token:
    :return:
    """
    # 判断用户名是否重复
    is_exist = check_modify_duplicate(account, email, phone, username)
    if is_exist['message'] != MESSAGE_DICT.SUCCESS:
        return {"message": MESSAGE_DICT.REPEAT.format(",".join(is_exist['message']))}

    update_json = {"username": username, "email": email, "phone": phone,
                   "image": image, "introduce": introduce,
                   "profession": profession, "member_level": member_level}
    old_info = User.find_one(account=account, is_delete=False)
    if not old_info:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("用户信息")}

    # 用户信息修改完成后，token也会随之更新，需要重新登录。
    if User.update(account=account, update_json=update_json):
        if Token.update(account=account, token=new_token):
            redis_cache.delete(f"token:{new_token}")
            return {"message": MESSAGE_DICT.SUCCESS}

    return {'message': MESSAGE_DICT.OPERATION_FAIL.format('修改用户信息')}




# def count_message(account, user_type):
#     sql = MySQLManager()
#     if user_type == 'student':
#         status = (1, 4, 5)
#         total = sql.Find(f"SELECT COUNT(*) AS total FROM session "
#                          f"WHERE student = '{account}' "
#                          f"AND status IN {status} "
#                          f"AND is_read = 0", False).get('total') or 0
#         sql.conn.close()
#         return {"message": MESSAGE_DICT.SUCCESS, 'total': total}
#     elif user_type == 'company':
#         status = (0, 2, 3, 6, 7, 8)
#         total = sql.Find(f"SELECT COUNT(*) AS total FROM session "
#                          f"WHERE company_id = '{account}' "
#                          f"AND status IN {status} "
#                          f"AND is_read = 0", False).get('total') or 0
#         sql.conn.close()
#         return {"message": MESSAGE_DICT.SUCCESS, 'total': total}


if __name__ == '__main__':
    pass
