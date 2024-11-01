# -------------------------------------导包--------------------------------------

from flask_app.databases import MySQLManager, RedisManager
from flask_app import MESSAGE_DICT

# ------------------------------------静态配置-----------------------------------
redis = RedisManager()
token_lives = 60 * 60 * 24 * 7
login_limit_time = 60 * 15


# -------------------------------------代码--------------------------------------
def get_class_list(account, skip, limit):
    sql = MySQLManager()
    teacher = sql.Find(f"SELECT account, class_id, class_name FROM user "
                       f"LEFT JOIN class ON user.class_id = class.id "
                       f"WHERE account = '{account}' "
                       f"AND user_type = 'teacher'", False)
    if not teacher:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("教师")}
    class_id = teacher.get("class_id")
    if not class_id:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("班级")}
    sql_str = f"SELECT * FROM user " \
              f"LEFT JOIN resume ON user.account = resume.account " \
              f"WHERE class_id = '{class_id}' " \
              f"AND user_type = 'student'"
    total = sql.Find(sql_str.replace('*', "count(*) AS total"), False)['total']
    if skip and limit:
        sql_str += f"ORDER BY create_time LIMIT {limit} OFFSET {skip}"
    result = sql.Find(sql_str)
    return {"message": MESSAGE_DICT.SUCCESS, "result": result,
            'total': total, 'class_name': teacher.get("class_name")}


def get_work_percent(class_id):
    if not class_id:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("您的班级")}
    sql = MySQLManager()
    sql_str = f"SELECT count(*) AS total FROM user " \
              f"LEFT JOIN resume ON user.account = resume.account " \
              f"WHERE user_type = 'student' " \
              f"AND class_id = '{class_id}'"
    total_student = sql.Find(sql_str, False)['total']
    if not total_student:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("您的学生")}
    total_worked = sql.Find(sql_str + ' AND is_worked = 1', False)['total']
    work_desc = '就业人数过半，请继续加油' if total_worked > 0.5 * total_student \
        else "就业人数过少, 请密切关注"
    sql.conn.commit()
    return {"message": MESSAGE_DICT.SUCCESS,
            "result": [{'name': '就业人数',
                        "value": total_worked},
                       {'name': '未就业人数',
                        "value": total_student - total_worked}],
            'workDesc': work_desc}


def get_work_by_keyword(class_id, group_keyword):
    if not class_id:
        return {"message": MESSAGE_DICT.NOT_FOUND.format("您的班级")}
    sql = MySQLManager()
    sql_str = f"SELECT {group_keyword}, count(*) AS total, " \
              f"AVG(salary) as salary " \
              f"FROM student_job LEFT JOIN user ON " \
              f"user.account = student_job.student " \
              f"WHERE user_type = 'student' " \
              f"AND class_id = '{class_id}' " \
              f"GROUP BY {group_keyword}"
    res = sql.Find(sql_str)
    sql.conn.close()
    if res:
        return {"message": MESSAGE_DICT.SUCCESS, "result": res}


if __name__ == '__main__':
    print(get_work_city('c9117788-fadf-11ee-a574-c91c309b7b94'))
