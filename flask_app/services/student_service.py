from flask_app.databases import student_db
from flask_app.services import get_token_info, page_limit_skip
from flask_app import MESSAGE_DICT


def get_resume(token, account):
    if not account:
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    return student_db.get_resume(account)


def add_resume(account, token, name, phone, education, major, work, city,
               email, skill, award, practice, salary, image, gender, birth):
    if not account:
        return {'message': MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if not info:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if account != info.get('account'):
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    if info.get('user_type') not in ['student', 'admin']:
        return {"message": MESSAGE_DICT.NOT_AUTH.format('简历上传')}
    if not all([name, phone, education, major,
                work, city, email, salary, image, gender, birth]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    salary = str(salary)
    res = student_db.add_resume(account, name, phone, education, major,
                                work, city, email, skill,
                                award, practice, salary, image, gender, birth)
    return res


def get_invite(token, account, is_read, page, limit):
    if not all([token, account]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('user_type') != 'student' or info.get("account") != account:
        return {"message": MESSAGE_DICT.NOT_AUTH.format('获取邀请信息')}
    skip, limit = page_limit_skip(page, limit)
    res = student_db.get_invite(account, is_read, skip, limit)
    return res


def get_work(token, account):
    if not all([token, account]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get("account") != account:
        return {"message": MESSAGE_DICT.TOKEN_ERROR}
    res = student_db.get_work(account)
    return res


def induction_work(token, session_id, student, company_name,
                   work_name, city, salary, work):
    if not all([token, student, company_name, work_name,
                city, salary, work]):
        return {"message": MESSAGE_DICT.PARAMS_ERROR}
    info = get_token_info(token)
    if info.get('user_type') != 'student' or info.get("account") != student:
        return {"message": MESSAGE_DICT.NOT_AUTH.format('获取邀请信息')}
    res = student_db.induction_work(session_id, student, company_name,
                                    work_name, city, salary, work)
    return res
