from flask_app.databases import teacher_db
from flask_app.services import get_token_info, page_limit_skip
from flask_app import MESSAGE_DICT


def get_class_list(token, account, page, limit):
    info = get_token_info(token)
    if info.get('account') != account or info.get('user_type') != 'teacher':
        return {'message': MESSAGE_DICT.TOKEN_ERROR}
    skip, limit = page_limit_skip(page, limit)
    return teacher_db.get_class_list(account, skip, limit)


def get_work_percent(token, account):
    info = get_token_info(token)
    if info.get('account') != account or info.get('user_type') != 'teacher':
        return {'message': MESSAGE_DICT.TOKEN_ERROR}
    return teacher_db.get_work_percent(info.get("class_id"))


def get_work_by_keyword(token, account, group_keyword):
    info = get_token_info(token)
    if info.get('account') != account or info.get('user_type') != 'teacher':
        return {'message': MESSAGE_DICT.TOKEN_ERROR}
    return teacher_db.get_work_by_keyword(info.get("class_id"), group_keyword)
