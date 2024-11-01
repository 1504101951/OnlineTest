# -------------------------------------导包--------------------------------------
from flask_app.databases import MySQLManager, RedisManager
from flask_app import MESSAGE_DICT

# ------------------------------------静态配置-----------------------------------
redis = RedisManager()
token_lives = 60 * 60 * 24 * 7
login_limit_time = 60 * 15


# -------------------------------------代码--------------------------------------
def get_resume(account):
    sql = MySQLManager()
    result = sql.Find(f"SELECT * FROM resume where account = '{account}'",
                      False)
    if 'salary' in result:
        result['salary'] = eval(result['salary'])
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result}


def add_resume(account, name, phone, education, major, work, city, email, skill,
               award, practice, salary, image, gender, birth):
    sql = MySQLManager()
    result = sql.Find(f"SELECT * FROM resume where account = '{account}'")
    # 如果查到重复的直接删了再加， 这样就可以做到编辑效果
    if result:
        sql.Exec(f"DELETE FROM resume where account = '{account}'")
    result = sql.Insert('resume', account=account, name=name, phone=phone,
                        education=education, major=major, work=work,
                        city=city, email=email, skill=skill, award=award,
                        practice=practice, salary=salary, image=image,
                        gender=gender, birth=birth)
    sql.conn.commit()
    sql.conn.close()
    if not result:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("简历上传")}
    return {"message": MESSAGE_DICT.SUCCESS}


def get_invite(account, is_read, skip, limit):
    sql = MySQLManager()
    sql_str = f"SELECT * FROM session " \
              f"WHERE student='{account}' "
    if is_read in ['0', '1', 0, 1]:
        sql_str += f' AND is_read = {int(is_read)}'
    total = sql.Find(sql_str.replace('*', 'count(*) AS total'),
                     False)['total'] or 0
    sql_str += f" ORDER BY is_read ASC, update_time DESC" \
               f" LIMIT {limit} OFFSET {skip}"
    result = sql.Find(sql_str)
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result, 'total': total}


def get_work(account):
    sql = MySQLManager()
    result = sql.Find(f"SELECT * FROM student_job where student = '{account}'",
                      False)
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result}


def induction_work(session_id, student, company_name,
                   work_name, city, salary, work):
    sql = MySQLManager()
    if session_id:
        res = sql.Exec(f"UPDATE session SET status = 6, "
                       f"is_read = 0 WHERE id = '{session_id}'")
        if not res:
            return {"message": MESSAGE_DICT.OPERATION_FAIL.format('入职')}
    sql.Exec(f"UPDATE session SET status = 8, is_read = 0 "
             f"WHERE id <> '{session_id}'")

    is_exist = sql.Find(f"SELECT * FROM student_job WHERE student= '{student}'")
    if is_exist:
        return {"message": MESSAGE_DICT.REPEAT.format('入职')}
    res = sql.Insert('student_job',
                     student=student, company_name=company_name,
                     work_name=work_name, city=city, salary=salary, work=work)
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format('入职')}
    return {"message": MESSAGE_DICT.SUCCESS}
