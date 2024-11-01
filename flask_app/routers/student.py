# -------------------------------------导包--------------------------------------
from flask import request
from flask_restx import Namespace, Resource

from flask_app.routers import response
from flask_app.services import student_service

# -------------------------------------常量--------------------------------------
student = Namespace("student", path='/student', description='学生模块')


# -------------------------------------代码--------------------------------------
@student.route('/resume/<account>')
class Login(Resource):
    def get(self, account):
        """
        查看学生简历
        :return:
        """
        token = request.headers.get('Authorization')
        result = student_service.get_resume(token, account)
        return response(result)

    def post(self, account):
        """
        上传/修改简历
        :return:
        """

        token = request.headers.get('Authorization')
        data = request.get_json()
        name = data.get("name")
        phone = data.get("phone")
        education = data.get("education")
        major = data.get('major')
        work = data.get("work")
        city = data.get('city')
        email = data.get('email')
        skill = data.get('skill') or ''
        award = data.get('award') or ''
        practice = data.get('practice') or ''
        salary = data.get('salary')
        image = data.get('image')
        gender = data.get('gender')
        birth = data.get('birth')
        result = student_service.add_resume(account, token,
                                            name, phone, education, major,
                                            work, city, email, skill,
                                            award, practice, salary, image,
                                            gender, birth)
        return response(result)


@student.route('/invite')
class Invite(Resource):
    def get(self):
        """
        查看学生收到的邀请
        :return:
        """
        token = request.headers.get('Authorization')
        account = request.args.get("account")
        is_read = request.args.get("is_read")
        page = request.args.get("page") or 1
        limit = request.args.get("limit") or 10
        result = student_service.get_invite(token, account, is_read, page,
                                            limit)
        return response(result)


@student.route('/work')
class Work(Resource):
    def get(self):
        """
        查看学生工作
        :return:
        """
        token = request.headers.get('Authorization')
        account = request.args.get("student")
        result = student_service.get_work(token, account)
        return response(result)

    def post(self):
        token = request.headers.get('Authorization')
        data = request.get_json()
        session_id = data.get("session_id")
        student_account = data.get("student")
        company_name = data.get("company_name")
        work_name = data.get("work_name")
        city = data.get("city")
        salary = data.get("salary")
        work = data.get('work')
        result = student_service.induction_work(token, session_id,
                                                student_account, company_name,
                                                work_name, city,
                                                salary, work)
        return response(result)
