# -------------------------------------导包--------------------------------------
import base64

from flask_app.databases import user_db
from flask_app.services import encrypt_pass, validate_params, create_token, \
    get_token_info
from flask_app import MESSAGE_DICT

# ------------------------------------静态配置-----------------------------------
default_path = '/default.jpg'


# -------------------------------------代码--------------------------------------
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


def register(account, username, password, check_passwd, sex, image, phone, email,
             introduce, profession):
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
    :return:
    """
    res = user_db.register(account, username, password, sex, image, phone, email,
                           introduce, profession, None)
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
    token = create_token(account, username, email,
                         phone, profession, member_level=0)

    res = user_db.register(account, username, password, sex, image, phone, email,
                           introduce, profession, None)

    return res


def check_pass(passwd, check_passwd):

    # 判断两次密码输入是否一致
    if passwd != check_passwd:
        return {"message": MESSAGE_DICT.CHECK_PASSWD_ERROR}

    # 判断密码是否合规
    check_param = validate_params(passwd=passwd)
    if check_param != MESSAGE_DICT.SUCCESS:
        return {"message": check_param}

    # 密码加密
    passwd = encrypt_pass(passwd)
    return {'message': MESSAGE_DICT.SUCCESS, 'passwd': passwd}


def modify_pass(account, user_type, old_pass, passwd, check_passwd, token):
    """
    :param account:
    :param old_pass:
    :param passwd:
    :param user_type:
    :param check_passwd:
    :param token:
    :return:
    """
    if not all([account, old_pass, passwd, check_passwd, token]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('account') != account:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}

    if info.get('user_type') not in [user_type, 'admin']:
        return {"message": MESSAGE_DICT.NOT_AUTH.format('修改密码')}
    old_pass = encrypt_pass(old_pass)
    passwd = check_pass(passwd, check_passwd)
    if passwd.get('message') != MESSAGE_DICT.SUCCESS:
        return passwd
    passwd = passwd.get('passwd')
    return user_db.modify_pass(account, old_pass, passwd, user_type)


def modify_info(auth_account, account, username, image, email, phone, user_type,
                introduce, class_id, token):
    """
    :param auth_account:
    :param account:
    :param username:
    :param image:
    :param email:
    :param phone:
    :param user_type:
    :param introduce:
    :param class_id:
    :param token:
    :return:
    """
    # 判断是否全部传入参数
    if not all([auth_account, account, username, image, email, phone,
                user_type, token]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}

    # 判断token和前端传的account是否一致
    info = get_token_info(token)

    # 先判断能否获取token
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}

    # 如果非管理员账户
    if info.get("user_type") != 'admin':
        if info.get("account") != auth_account:
            # 判断前端传递的账号是否跟密钥里的一致
            return {"message": MESSAGE_DICT.TOKEN_ERROR}
        if user_type != info.get("user_type"):
            # 判断前端传的user_type是否跟token一致
            return {"message": MESSAGE_DICT.TOKEN_ERROR}

    # 判断参数是否合规
    check_param = validate_params(account=account, email=email, phone=phone)
    if check_param != MESSAGE_DICT.SUCCESS:
        return {"message": check_param}

    # 通过修改后的用户信息获取新的token
    new_token = create_token(account, username, email, phone,
                             user_type, introduce, class_id)

    res = user_db.modify_info(account, username, image, email, phone,
                              user_type, introduce, class_id, new_token)
    return res


def get_image(username, token):
    user = get_token_info(token)
    if not user:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if user.get("account") == username:
        return user_db.get_image(username)


def upload_image(file):
    if not file:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("头像文件")}
    file = str(base64.b64encode(file.read()))[2:].replace('\'', '')
    image = "data:image/jpeg;base64," + file
    return {"image": image, "message": MESSAGE_DICT.SUCCESS}


def count_message(token, account):
    if not all([token, account]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info or info.get('account') != account:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    user_type = info.get('user_type')
    return user_db.count_message(account, user_type)
