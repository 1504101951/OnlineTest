from flask_app.databases import admin_db
from flask_app.services import get_token_info, page_limit_skip, create_token
from flask_app import MESSAGE_DICT


def check_admin(token, account, module):
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if info.get("user_type") != 'admin' or info.get("account") != account:
        return {"message": MESSAGE_DICT.NOT_AUTH.format(module)}
    return {"message": MESSAGE_DICT.SUCCESS}


def get_user_list(token, user_type, account, page, limit):
    check_message = check_admin(token, account, '查看用户列表')
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message
    skip, limit = page_limit_skip(page, limit)
    return admin_db.get_user_list(user_type, skip, limit)


def set_user_class(token, account, user_account, user_type, class_id):
    if not all([token, account, user_account, user_type, class_id]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if info.get("user_type") != 'admin' or info.get("account") != account:
        return {"message": MESSAGE_DICT.NOT_AUTH.format('设置用户班级')}
    if class_id:
        info.update({"class_id": class_id})
    new_token = create_token(**info)
    if user_type not in ['student', 'teacher']:
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    return admin_db.set_user_class(user_account, class_id, new_token)


def delete_user(token, account, user_account):
    # 检查权限
    check_message = check_admin(token, account, '删除用户')
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message
    return admin_db.delete_user(user_account)


def get_school_info():
    return admin_db.get_school_info()


def set_school_info(school_name, account, email, phone, school_image, token):
    # 校验参数
    if not all([school_name, school_image, account, token, email, phone]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}

    # 校验token
    check_message = check_admin(token, account, '修改学校信息')
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message

    return admin_db.set_school_info(school_name, school_image, email, phone)


def get_class_list(token, account, page, limit):
    if not all([token, account]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    check_message = check_admin(token, account, '查看教室列表')
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message
    if page and limit:
        skip, limit = page_limit_skip(page, limit)
    else:
        skip = None
    return admin_db.get_class_list(skip, limit)


def create_class(token, account, class_name):
    if not all([token, account, class_name]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    check_message = check_admin(token, account, '新增教室')
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message
    return admin_db.create_class(class_name)


def get_class_details(token, account, class_id, page, limit):
    if not all([token, account, class_id]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    check_message = check_admin(token, account, '查看教室详情')
    skip, limit = page_limit_skip(page, limit)
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message
    return admin_db.get_class_details(class_id, skip, limit)


def update_class(token, account, class_id, class_name):
    if not all([token, account, class_id, class_name]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    check_message = check_admin(token, account, '修改教室名称')
    if check_message.get("message") != MESSAGE_DICT.SUCCESS:
        return check_message
    return admin_db.update_class(class_id, class_name)
