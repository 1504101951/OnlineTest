# -------------------------------------导包--------------------------------------
from flask import request
from flask_restx import Namespace, Resource

from flask_app.routers import response
from flask_app.services import teacher_service

# -------------------------------------常量--------------------------------------
teacher = Namespace("teacher", path='/teacher', description='教师模块')


# -------------------------------------代码--------------------------------------
@teacher.route('/class')
class ClassInfo(Resource):
    def get(self):
        """
        获取班级信息
        :return:
        """
        token = request.headers.get('Authorization')
        account = request.args.get('account')
        page = request.args.get('page') or 1
        limit = request.args.get('limit') or 10
        res = teacher_service.get_class_list(token, account, page, limit)
        return response(res)


@teacher.route("/jobPercent")
class JobPercent(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        account = request.args.get('account')
        res = teacher_service.get_work_percent(token, account)
        return response(res)


@teacher.route("/job")
class WorkByKeyword(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        account = request.args.get('account')
        group_keyword = request.args.get('group_keyword')
        res = teacher_service.get_work_by_keyword(token, account, group_keyword)
        return response(res)
