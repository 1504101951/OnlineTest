# -------------------------------------导包--------------------------------------
from sqlalchemy import or_, union, select, literal_column

from flask_app.databases import redis_cache
from flask_app import MESSAGE_DICT
from flask_app.models.user_model import User
import pickle

# ------------------------------------静态配置-----------------------------------
token_lives = 60 * 60 * 24 * 7
login_limit_time = 60 * 15


# -----------------------------------内部调用方法---------------------------------
def check_duplicate(account, email, phone, username):
    errors = []
    # 检查账号是否重复
    if User.find_one(account=account):
        errors.append("账号已存在")

    # 检查邮箱是否重复
    if User.find_one(email=email):
        errors.append("邮箱已注册")

    # 检查手机号是否重复
    if User.find_one(phone=phone):
        errors.append("手机号已注册")

    # 检查用户名是否重复
    if User.find_one(username=username):
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
    if redis_cache.get(addr) not in [None, '1', '2', '3', '4', '5']:
        return {"message": MESSAGE_DICT.LOGIN_LIMIT}
    # 找数据库中匹配账号密码的用户
    entities = ['account', 'username', 'image', 'email', 'phone',
                'introduce', 'profession', 'sex', 'member_level']
    result = User.find_one(entities=entities, account=account, password=password, is_delete=False)
    # 找不到则视为(账号/密码)错误
    if not result:
        # 在redis中自增1， 防止同一个IP短时间内登录次数过多
        redis_cache.inc(addr, login_limit_time)
        return {"message": MESSAGE_DICT.LOGIN_ERROR}
    # 从数据库中获取token， 存放到redis中， 并设置过期时间为7天
    token = sql.Find("SELECT token FROM token "
                     f"WHERE account = '{account}'", False).get("token")
    # 如果token设置失败, 则视为登录失败, 序列化value
    if not redis_cache.set(token, pickle.dumps(result), ex_time=token_lives):
        return {"message": MESSAGE_DICT.LOGIN_ERROR}
    # redis删除登录失败次数
    redis_cache.delete(addr)
    # 成功， 返回提示信息与token
    return {"message": MESSAGE_DICT.SUCCESS, "token": token,
            'result': result}


def get_user_info(account):
    """
    获取用户信息
    :param account:
    :return:
    """
    sql = MySQLManager()
    result = sql.Find(f"SELECT * FROM user LEFT JOIN "
                      f"class ON class.id = user.class_id "
                      f"WHERE is_delete = False "
                      f"AND is_active = True "
                      f"AND account = '{account}' ",
                      False)
    sql.conn.close()
    if not result:
        return {"message": MESSAGE_DICT.NOT_FOUND}
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result}


def register(account, username, password, sex, image, phone, email,
             introduce, profession, token):
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
    :param token: 用户密钥
    :return:
    """
    is_exist = check_duplicate(account, email, phone, username)
    if is_exist['message'] != MESSAGE_DICT.SUCCESS:
        return {"message": MESSAGE_DICT.REPEAT.format(",".join(is_exist['message']))}

    # 创建用户
    create_user = User.create(account=account, username=username, password=password,
                              sex=sex, image=image, phone=phone, email=email,
                              introduce=introduce, profession=profession)

    # 如果创建失败则返回报错信息
    if not create_user:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("注册")}
    # 创建成功则继续创建token
    create_token = sql.Insert('token', account=account, token=token)
    # 如果创建失败则返回报错信息并删除创建成功的用户
    if not create_token:
        sql.Exec(f"DELETE FROM user WHERE account = '{account}'")
        sql.conn.close()
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("注册")}
    sql.conn.commit()
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS}


def modify_pass(account, old_pass, passwd, user_type):
    sql = MySQLManager()
    if old_pass == passwd:
        return {"message": MESSAGE_DICT.SUCCESS}
    is_valid = sql.Find(f"SELECT account, passwd from user "
                        f"WHERE account = '{account}' "
                        f"AND passwd = '{old_pass}' "
                        f"AND user_type = '{user_type}'")
    if not is_valid:
        return {"message": MESSAGE_DICT.OLD_PASS_ERROR}

    res = sql.Exec(f"UPDATE user SET passwd = '{passwd}' "
                   f"WHERE account = '{account}' "
                   f"AND user_type = '{user_type}'")
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('修改密码')}
    return {'message': MESSAGE_DICT.SUCCESS}


def modify_info(account, username, image, email, phone,
                user_type, introduce, class_id, new_token):
    """
    修改账号信息
    :param account:
    :param username:
    :param image:
    :param email:
    :param phone:
    :param user_type:
    :param introduce:
    :param class_id:
    :param new_token:
    :return:
    """
    sql = MySQLManager()
    # 判断用户名是否重复
    find_repeat = sql.Find(f"SELECT '用户名' AS type FROM "
                           f"user WHERE username = '{username}' "
                           f"AND account <> '{account}' "
                           f"UNION "
                           f"SELECT '手机号' AS type FROM "
                           f"user WHERE phone = '{phone}' "
                           f"AND account <> '{account}' "
                           f"UNION "
                           f"SELECT '邮箱' AS type FROM "
                           f"user WHERE email = '{email}' "
                           f"AND account <> '{account}' ")
    if find_repeat:
        message = ",".join(find_repeat.values())
        return {"message": MESSAGE_DICT.REPEAT.format(message)}
    if class_id:
        find_str = f"AND class_id = {class_id}"
        update_str = f", class_id = '{class_id}' "
    else:
        find_str = ''
        update_str = ''
    is_update = sql.Find(f"SELECT * FROM user WHERE account = '{account}' "
                         f"AND image = '{image}' "
                         f"AND email = '{email}' "
                         f"AND phone = '{phone}' "
                         f"AND user_type = '{user_type}' "
                         f"AND introduce = '{introduce}' "
                         f"{find_str}", False)
    if is_update:
        return {"message": MESSAGE_DICT.SUCCESS}
    update_str = f"UPDATE user SET username = '{username}', " \
                 f"image = '{image}', " \
                 f"email = '{email}', " \
                 f"phone = '{phone}', " \
                 f"user_type = '{user_type}', " \
                 f"introduce = '{introduce}', " \
                 f"token = '{new_token}' {update_str}"
    update_str += f"WHERE account = '{account}'"
    res = sql.Exec(update_str)
    sql.conn.commit()
    sql.conn.close()
    # 用户信息修改完成后，token也会随之更新，需要重新登录。
    if not res:
        return {'message': MESSAGE_DICT.OPERATION_FAIL.format('修改用户信息')}
    return {"message": MESSAGE_DICT.SUCCESS}


def get_image(username):
    sql = MySQLManager()
    image = sql.Find(f"SELECT image from user WHERE username = '{username}'",
                     False)
    sql.conn.close()
    if not image:
        return {'message': MESSAGE_DICT.NOT_FOUND.format("用户头像")}
    return {"message": MESSAGE_DICT.SUCCESS, "result": image}


def count_message(account, user_type):
    sql = MySQLManager()
    if user_type == 'student':
        status = (1, 4, 5)
        total = sql.Find(f"SELECT COUNT(*) AS total FROM session "
                         f"WHERE student = '{account}' "
                         f"AND status IN {status} "
                         f"AND is_read = 0", False).get('total') or 0
        sql.conn.close()
        return {"message": MESSAGE_DICT.SUCCESS, 'total': total}
    elif user_type == 'company':
        status = (0, 2, 3, 6, 7, 8)
        total = sql.Find(f"SELECT COUNT(*) AS total FROM session "
                         f"WHERE company_id = '{account}' "
                         f"AND status IN {status} "
                         f"AND is_read = 0", False).get('total') or 0
        sql.conn.close()
        return {"message": MESSAGE_DICT.SUCCESS, 'total': total}


if __name__ == '__main__':
    register(None, None, None, None, None, None, None, None, None)
