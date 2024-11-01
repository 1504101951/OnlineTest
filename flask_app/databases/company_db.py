# -------------------------------------导包--------------------------------------
from flask_app.databases import MySQLManager, RedisManager
from flask_app import MESSAGE_DICT

# ------------------------------------静态配置-----------------------------------
redis = RedisManager()
token_lives = 60 * 60 * 24 * 7
login_limit_time = 60 * 15


# -------------------------------------代码--------------------------------------
def find_list(count_str, sql_str):
    sql = MySQLManager()
    total = sql.Find(count_str, False)['total'] or 0
    result = sql.Find(sql_str)
    sql.conn.close()
    return {'message': MESSAGE_DICT.SUCCESS, 'result': result, 'total': total}


def find_work_by_id(work_id):
    sql = MySQLManager()
    result = sql.Find(f"SELECT * FROM WORK WHERE id = '{work_id}'", False)
    if not result:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("该岗位信息")}
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result}


def publish_work(work_id, account, company_name, title, education, major, work,
                 city, welfare, responsibility, requirement, image, salary):
    sql = MySQLManager()
    if work_id:
        is_exist = sql.Find(f"SELECT * FROM work where id = '{work_id}'")
        if is_exist:
            sql.Exec(f"UPDATE work SET company_id = '{account}', "
                     f"company_name = '{company_name}', "
                     f"title = '{title}', "
                     f"education = '{education}', major = '{major}', "
                     f"work ='{work}', city='{city}', "
                     f"welfare = '{welfare}', "
                     f"responsibility = '{responsibility}', "
                     f"requirement = {requirement}, "
                     f"image='{image}', "
                     f"salary='{salary}' "
                     f"WHERE id = '{work_id}'")
    else:
        result = sql.Insert('work', company_id=account,
                            company_name=company_name,
                            title=title, education=education, major=major,
                            work=work, city=city, welfare=welfare,
                            responsibility=responsibility,
                            requirement=requirement, image=image,
                            salary=salary)
        if not result:
            return {"message": MESSAGE_DICT.OPERATION_FAIL.format("岗位发布")}
    sql.conn.commit()
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS}


def delete_work_by_id(work_id):
    sql = MySQLManager()
    res = sql.Exec(f"DELETE FROM work WHERE id = '{work_id}' ")
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("岗位删除")}
    return {"message": MESSAGE_DICT.SUCCESS}


def find_session(account, work_id, skip, limit):
    sql = MySQLManager()
    sql_str = f"SELECT * FROM session WHERE company_id = '{account}' "
    if work_id:
        sql_str += f"AND work_id = '{work_id}' "
    total = sql.Find(sql_str.replace('*', 'count(*) AS total'),
                     False).get('total') or 0
    sql_str += f'ORDER BY is_read ASC, work_id DESC LIMIT {limit} OFFSET {skip}'
    res = sql.Find(sql_str)
    sql.conn.close()
    return {'message': MESSAGE_DICT.SUCCESS, 'result': res, 'total': total}


def create_session(student, company_id, company_name, work_id, work_name,
                   status, place, date):
    sql = MySQLManager()
    is_resume = sql.Find(f"SELECT * FROM resume "
                         f"WHERE account = '{student}' "
                         f"AND is_worked = 0", False)
    if not is_resume:
        return {"message": MESSAGE_DICT.NOT_FOUND.format('简历')}
    is_exist = sql.Find(f"SELECT * FROM session WHERE "
                        f"work_id = '{work_id}' "
                        f"AND student = '{student}'", False)
    if is_exist:
        return {"message": MESSAGE_DICT.REPEAT.format('该会话')}
    res = sql.Insert('session', student=student, company_id=company_id,
                     company_name=company_name, work_id=work_id,
                     work_name=work_name, status=status, place=place, date=date)
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('会话创建')}
    return {"message": MESSAGE_DICT.SUCCESS}


def push_session(session_id, status, place, date):
    sql = MySQLManager()
    sql_str = f"UPDATE session SET status = {status}, is_read = 0 "
    if place and date:
        sql_str += f",place = '{place}', date = '{date}' "
    sql_str += f"WHERE id = '{session_id}'"
    res = sql.Exec(sql_str)
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('确认')}
    return {"message": MESSAGE_DICT.SUCCESS}


def find_resume_details(session_id):
    sql = MySQLManager()
    resume = sql.Find(f"SELECT * FROM resume "
                      f"INNER JOIN session "
                      f"ON session.student = resume.account "
                      f"WHERE session.id = '{session_id}' "
                      f"AND is_worked=0", False)
    sql.conn.close()
    if not resume:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("简历")}
    return {"message": MESSAGE_DICT.SUCCESS, 'result': resume}


def read_resume(session_id):
    sql = MySQLManager()
    res = sql.Exec(f"UPDATE session SET is_read = 1 "
                   f"WHERE id = '{session_id}'")
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('简历标记已读')}
    return {"message": MESSAGE_DICT.SUCCESS}


def post_invite(company, student, session_id, place, date):
    sql = MySQLManager()
    is_exist = sql.Find(f"SELECT * FROM session "
                        f"WHERE student = '{student}' "
                        f"AND company = '{company}' "
                        f"AND session_id = '{session_id}' ")
    if is_exist:
        return {"message": MESSAGE_DICT.REPEAT.format('面试邀请')}

    is_worked = sql.Find(f"SELECT * FROM resume WHERE account = '{student}' "
                         f"AND is_worked = 1", False)
    if is_worked:
        return {"message": MESSAGE_DICT.WORKED.format('已工作')}

    res = sql.Exec(f"UPDATE session SET status = 1, place = '{place}', "
                   f"date= '{date}' "
                   f"AND is_read = 0 "
                   f"WHERE id = '{session_id}' ")
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('面试邀请')}
    return {"message": MESSAGE_DICT.SUCCESS}


def delete_session(session_id):
    sql = MySQLManager()
    res = sql.Exec(f"DELETE FROM session "
                   f"WHERE id = '{session_id}'")
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('面试邀请')}
    sql.conn.commit()
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS}


if __name__ == '__main__':
    pass
