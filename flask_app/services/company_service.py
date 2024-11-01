from flask_app.databases import company_db
from flask_app.services import get_token_info, page_limit_skip, time_format
from flask_app import MESSAGE_DICT


def get_resume(token, name, major, education,
               city, work, page, limit):
    sql_str = "SELECT * FROM resume LEFT JOIN user " \
              "ON resume.account = user.account " \
              "WHERE is_worked=0 "
    param_list = []
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if info.get("user_type") == 'teacher':
        class_id = info.get("class_id")
        if class_id:
            param_list.append(f"class_id = '{class_id}'")
    if name:
        param_list.append(f"name like '%{name}%'")
    if major:
        param_list.append(f"major = '{major}'")
    if work:
        param_list.append(f"work = '{work}'")
    if education:
        param_list.append(f"education = '{education}'")
    if city:
        param_list.append(f"city = '{city}'")
    if param_list:
        sql_str += f'AND {" AND ".join(param_list)}'
    skip, limit = page_limit_skip(page, limit)
    count_str = sql_str.replace('*', "count(*) AS total")
    sql_str += f" ORDER BY resume.update_time DESC LIMIT {limit} OFFSET {skip}"
    res = company_db.find_list(count_str, sql_str)
    return res


def find_work(token, title, company_id, major, education,
              city, work, page, limit):
    info = get_token_info(token)
    sql_str = "SELECT * FROM WORK "
    param_list = []
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if company_id:
        param_list.append(f"company_id = '{company_id}'")
    if title:
        param_list.append(f"title like '%{title}%'")
    if major:
        param_list.append(f"major = '{major}'")
    if education:
        param_list.append(f"education = '{education}'")
    if city:
        param_list.append(f"city = '{city}'")
    if work:
        param_list.append(f"work = '{work}'")
    if param_list:
        sql_str += f'WHERE {" AND ".join(param_list)}'
    skip, limit = page_limit_skip(page, limit)
    count_str = sql_str.replace('*', "count(*) AS total")
    sql_str += f" ORDER BY update_time DESC LIMIT {limit} OFFSET {skip}"
    res = company_db.find_list(count_str, sql_str)
    return res


def publish_work(token, work_id, account, company_name, title, education,
                 major, work, city, welfare,
                 responsibility, requirement, image,
                 salary):
    if not all([token, account, company_name, title, education, major, work,
                city, welfare, responsibility, requirement, image, salary]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if account != info.get('account'):
        return {'message': MESSAGE_DICT.TOKEN_ERROR}
    salary = '-'.join(map(str, salary)).replace('000', 'k')
    res = company_db.publish_work(work_id, account, company_name, title,
                                  education, major, work, city, welfare,
                                  responsibility, requirement, image,
                                  salary)
    return res


def find_work_by_id(token, work_id):
    if not all([token, work_id]):
        return MESSAGE_DICT.PARAMS_ERROR
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    res = company_db.find_work_by_id(work_id)
    return res


def delete_work_by_id(token, account, work_id):
    if not all([token, account, work_id]):
        return MESSAGE_DICT.PARAMS_ERROR
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if info.get('account') != account:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    res = company_db.delete_work_by_id(work_id)
    return res


def find_session(token, account, work_id, page, limit):
    if not all([token, account]):
        return {'message': MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('account') != account and info.get("user_type") != 'company':
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    skip, limit = page_limit_skip(page, limit)
    res = company_db.find_session(account, work_id, skip, limit)
    return res


def create_session(token, student, company_id, company_name, work_id,
                   work_name, status, place, date):
    if not all([token, student, company_id, company_name, work_id, work_name]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if date:
        date = time_format(date)
    res = company_db.create_session(student, company_id, company_name, work_id,
                                    work_name, status, place, date)
    return res


def push_session(token, account, session_id, status, place, date):
    if not all([token, account, session_id, status]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('account') != account:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if date:
        date = time_format(date)
    res = company_db.push_session(session_id, status, place, date)
    return res


def find_resume_details(token, account, session_id):
    if not all([token, account, session_id]):
        return MESSAGE_DICT.PARAMS_ERROR
    info = get_token_info(token)
    if info.get('account') != account and info.get("user_type") != 'company':
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    res = company_db.find_resume_details(session_id)
    return res


def read_resume(token, account, session_id):
    if not all([token, account, session_id]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('account') != account and info.get("user_type") != 'company':
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    res = company_db.read_resume(session_id)
    return res


def delete_session(token, account, session_id):
    if not all([token, account, session_id]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('user_type') != 'company' or info.get("account") != account:
        return {"message": MESSAGE_DICT.NOT_AUTH.format('删除邀请')}
    res = company_db.delete_session(session_id)
    return res


if __name__ == '__main__':
    find_dict = {"salary": '1',
                 'account': 2}
