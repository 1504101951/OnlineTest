# -------------------------------------导包--------------------------------------
import base64

from flask_app.databases import user_db
from flask_app.services import encrypt_pass, validate_params, create_token, \
    get_token_info, check_pass, save_file, remove_file
from flask_app import MESSAGE_DICT

# ------------------------------------静态配置-----------------------------------
default_path = '/default.jpg'


# ---------------------------------接口调用方法-----------------------------------
def login(account, password, addr):
    if not all([account, password, addr]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    password = encrypt_pass(password)
    if not password:
        return {"message": MESSAGE_DICT.PARAMS_NOT_VALID.format(password)}
    return user_db.login(account, password, addr)


def get_user_info(token, account):
    if not account:
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    return user_db.get_user_info(account)


def register(account, username, password, check_passwd, sex, image, phone,
             email, introduce, profession, is_admin):
    """
    :param account:
    :param username:
    :param password:
    :param check_passwd:
    :param sex:
    :param image:
    :param email:
    :param phone:
    :param introduce:
    :param profession:
    :param is_admin:
    :return:
    """
    # 判断两次密码输入是否一致
    if password != check_passwd:
        return {"message": MESSAGE_DICT.CHECK_PASSWD_ERROR}

    # 判断所有参数是否都传入
    if not all([account, username, password, check_passwd, image, phone, email,
                introduce, profession]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    # 校验每个参数是否合规
    check_params = validate_params(account, password, email, phone)
    if check_params != MESSAGE_DICT.SUCCESS:
        return {"message": check_params}

    # 加密密码
    password = encrypt_pass(password)

    # 生成token
    token = create_token(account, username, email, phone, introduce, profession, image)

    res = user_db.register(account, username, password, sex, image, phone,
                           email, introduce, profession, is_admin, token)
    return res


def modify_pass(account, old_pass, password, check_passwd, token):
    """
    :param account:
    :param old_pass:
    :param password:
    :param check_passwd:
    :param token:
    :return:
    """
    if not all([account, old_pass, password, check_passwd, token]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)

    if info.get('account') != account:
        if not info.get("is_admin"):
            return {"message": MESSAGE_DICT.NOT_AUTH.format('修改密码')}

    old_pass = encrypt_pass(old_pass)
    password = check_pass(password, check_passwd)
    if password.get('message') != MESSAGE_DICT.SUCCESS:
        return password
    password = password.get('password')

    return user_db.modify_pass(account, old_pass, password, token)


def modify_info(account, username, email, phone, image, profession,
                introduce, member_level, is_admin, token):
    """
    :param account:
    :param username:
    :param email:
    :param phone:
    :param image:
    :param profession:
    :param introduce:
    :param member_level:
    :param is_admin:
    :param token:
    :return:
    """
    # 判断是否全部传入参数
    if not all([account, username, image, email, phone, token]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}

    # 判断token和前端传的account是否一致
    info = get_token_info(token)

    # 先判断能否获取token
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}

    # 如果非管理员账户
    if not info.get('is_admin'):
        # 非管理员用户不允许修改会员信息
        if member_level is not None:
            return {"message": MESSAGE_DICT.NOT_AUTH.format('修改会员等级信息')}
        # 只有管理员用户和本人才可以修改本人个人信息
        if not info.get('account') == account:
            return {"message": MESSAGE_DICT.NOT_AUTH.format('修改个人信息')}

    # 判断参数是否合规
    check_param = validate_params(account=account, email=email, phone=phone)
    if check_param != MESSAGE_DICT.SUCCESS:
        return {"message": check_param}

    # 通过修改后的用户信息获取新的token
    new_token = create_token(account, username, email, phone, introduce,
                             profession, image, member_level, is_admin)

    res = user_db.modify_info(account, username, email, phone, introduce,
                              profession, image, member_level, new_token)
    return res


def get_image(username, token):
    user = get_token_info(token)
    if not user:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if user.get("account") == username:
        return user_db.get_image(username)


def upload_image(image):
    if not image:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("头像文件")}
    return save_file("temp", image)


def count_message(token, account):
    if not all([token, account]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info or info.get('account') != account:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    user_type = info.get('user_type')
    return user_db.count_message(account, user_type)
