# -------------------------------------导包--------------------------------------
from flask import request
from flask_restx import Namespace, Resource
from flask_app.routers import response
from flask_app.services import admin_service

# -------------------------------------常量--------------------------------------
admin = Namespace("admin", path='/admin', description='管理员模块')


# -------------------------------------代码--------------------------------------
@admin.route("/userAdmin")
class UserAdmin(Resource):
    def get(self):
        """
        获取用户列表
        :return:
        """
        token = request.headers.get('Authorization')
        account = request.args.get("account")
        user_type = request.args.get("user_type")
        page = request.args.get("page") or 0
        limit = request.args.get('limit') or 10
        result = admin_service.get_user_list(token, user_type, account,
                                             page, limit)
        return response(result)

    def put(self):
        token = request.headers.get('Authorization')
        data = request.get_json()
        account = data.get('account')
        user_type = data.get("user_type")
        user_account = data.get("user_account")
        class_id = data.get('class_id')
        result = admin_service.set_user_class(token, account, user_account,
                                              user_type, class_id)
        return response(result)

    def delete(self):
        """
        删除用户
        :return:
        """
        token = request.headers.get("Authorization")
        data = request.get_json()
        account = data.get("account")
        user_account = data.get("user_account")
        result = admin_service.delete_user(token, account, user_account)
        return response(result)


@admin.route("/schoolInfo")
class SchoolInfo(Resource):
    def get(self):
        """
        获取学校信息
        :return:
        """
        result = admin_service.get_school_info()
        return response(result)

    def post(self):
        """
        设置学校信息
        :return:
        """
        data = request.get_json()
        token = request.headers.get('Authorization')
        school_name = data.get("school_name")
        school_image = data.get("school_image")
        email = data.get("email")
        phone = data.get("phone")
        account = data.get("account")
        result = admin_service.set_school_info(school_name, account, email,
                                               phone, school_image, token)
        return response(result)


@admin.route('/class')
class ClassInfo(Resource):
    def get(self):
        """
        获取班级列表
        :return:
        """
        token = request.headers.get('Authorization')
        account = request.args.get("account")
        page = request.args.get("page")
        limit = request.args.get('limit')
        result = admin_service.get_class_list(token, account, page, limit)
        return response(result)

    def post(self):
        """
        创建班级
        :return:
        """
        token = request.headers.get('Authorization')
        data = request.get_json()
        account = data.get("account")
        class_name = data.get("class_name")
        result = admin_service.create_class(token, account, class_name)
        return response(result)

    def put(self):
        """
        修改班级名称
        :return:
        """
        token = request.headers.get('Authorization')
        data = request.get_json()
        class_id = data.get("class_id")
        class_name = data.get("class_name")
        account = data.get("account")
        result = admin_service.update_class(token, account, class_id,
                                            class_name)
        return response(result)


@admin.route("/classDetails")
class ClassDetails(Resource):
    def get(self):
        """
        获取班级详情
        :return:
        """
        token = request.headers.get('Authorization')
        account = request.args.get("account")
        class_id = request.args.get("class_id")
        page = request.args.get("page") or 1
        limit = request.args.get('limit') or 10
        result = admin_service.get_class_details(token, account, class_id,
                                                 page, limit)
        return response(result)
