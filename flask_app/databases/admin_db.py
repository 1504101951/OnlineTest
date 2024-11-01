# -------------------------------------导包--------------------------------------
from flask_app.databases import redis_cache
from flask_app import MESSAGE_DICT
import pickle

# ------------------------------------静态配置-----------------------------------

token_lives = 60 * 60 * 24 * 7
login_limit_time = 60 * 15


# -------------------------------------代码--------------------------------------
def get_user_list(user_type, skip, limit):
    sql = MySQLManager()
    sql_str = "SELECT * " \
              "FROM user WHERE user_type <> 'admin' "
    sql_list = []
    if user_type:
        sql_list.append(f"user_type = '{user_type}' ")
    if sql_list:
        sql_str += f'AND {" AND ".join(sql_list)}'
    total = sql.Find(sql_str.replace('*', "COUNT(*) AS total"), False)['total']
    sql_str += f"LIMIT {limit} OFFSET {skip}"
    result = sql.Find(sql_str) or []
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS, 'result': result, 'total': total}


def set_user_class(user_account, class_id, new_token):
    sql = MySQLManager()
    res = sql.Exec(f"UPDATE user SET class_id = '{class_id}' ,"
                   f"token = '{new_token}' "
                   f"WHERE account = '{user_account}' ")
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("用户状态修改")}
    sql.conn.commit()
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS}


def delete_user(user_account):
    sql = MySQLManager()
    res = sql.Exec(f"DELETE FROM user WHERE account = '{user_account}'")
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("用户删除")}
    return {"message": MESSAGE_DICT.SUCCESS}


def get_school_info():
    result = redis_cache.get("school_info")
    if not result:
        return {"message": MESSAGE_DICT.NOT_FOUND.format('school_info')}
    return {"message": MESSAGE_DICT.SUCCESS, "result": result}


def set_school_info(school_name, school_image, email, phone):
    # 设置为永久有效
    if not redis_cache.set("school_info",
                     pickle.dumps({"school_name": school_name,
                                   "school_image": school_image,
                                   'email': email,
                                   "phone": phone}), ex_time=None):
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("学校信息修改")}
    return {"message": MESSAGE_DICT.SUCCESS}


def get_class_list(skip, limit):
    sql = MySQLManager()
    sql_str = "SELECT * FROM class "
    total = sql.Find(sql_str.replace('*', "COUNT(*) AS total"), False)['total']
    if skip and limit:
        sql_str += f'ORDER BY create_time DESC LIMIT {limit} OFFSET {skip}'
    result = sql.Find(sql_str) or []
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS, "result": result, 'total': total}


def create_class(class_name):
    sql = MySQLManager()
    is_exist = sql.Find(f"SELECT * FROM class "
                        f"WHERE class_name = '{class_name}'")
    if is_exist:
        return {"message": MESSAGE_DICT.REPEAT.format('班级')}
    res = sql.Insert('class', class_name=class_name)
    sql.conn.commit()
    sql.conn.close()
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("班级创建")}
    return {"message": MESSAGE_DICT.SUCCESS}


def get_class_details(class_id, skip, limit):
    sql = MySQLManager()
    class_info = sql.Find(f"SELECT * FROM class WHERE id = '{class_id}'", False)
    if not class_info:
        return {"message": MESSAGE_DICT.NOT_FOUND.format('班级')}
    sql_str = f"SELECT * FROM user WHERE class_id = '{class_id}' "
    total = sql.Find(sql_str.replace('*', "COUNT(*) AS total"), False)['total']
    sql_str += f"ORDER BY create_time DESC limit {limit} OFFSET {skip}"
    result = sql.Find(sql_str) or []
    return {"message": MESSAGE_DICT.SUCCESS,
            "result": result,
            'total': total,
            'class_info': class_info}


def update_class(class_id, class_name):
    sql = MySQLManager()
    res = sql.Exec(f"UPDATE class SET class_name = '{class_name}' "
                   f"WHERE id = '{class_id}'")
    if not res:
        return {"message": MESSAGE_DICT.OPERATION_FAIL.format("班级修改")}
    sql.conn.commit()
    sql.conn.close()
    return {"message": MESSAGE_DICT.SUCCESS}


if __name__ == '__main__':
    pass
