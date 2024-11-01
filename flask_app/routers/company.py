# -------------------------------------导包--------------------------------------
from flask import request
from flask_restx import Namespace, Resource

from flask_app.routers import response
from flask_app.services import company_service

# -------------------------------------常量--------------------------------------
company = Namespace("company", path='/company', description='企业模块')


# -------------------------------------代码--------------------------------------
@company.route("/work")
class Work(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        title = request.args.get("title")
        company_id = request.args.get("company_id")
        major = request.args.get("major")
        education = request.args.get("education")
        city = request.args.get("city")
        work = request.args.get("work")
        page = request.args.get('page') or 1
        limit = request.args.get('limit') or 10
        result = company_service.find_work(token, title, company_id, major,
                                           education, city, work,
                                           page, limit)
        return response(result)

    def post(self):
        """
        岗位发布
        :return:
        """
        data = request.get_json()
        token = request.headers.get('Authorization')
        work_id = data.get('id') or None
        account = data.get("account")
        company_name = data.get("company")
        title = data.get("title")
        education = data.get('education')
        major = data.get("major")
        work = data.get("work")
        city = data.get('city')
        welfare = data.get("welfare")
        responsibility = data.get("responsibility")
        requirement = data.get("requirement")
        image = data.get('image')
        salary = data.get("salary")
        result = company_service.publish_work(token, work_id,
                                              account, company_name,
                                              title, education,
                                              major, work, city, welfare,
                                              responsibility, requirement,
                                              image,
                                              salary)
        return response(result)


@company.route('/work/<work_id>')
class WorkById(Resource):
    def get(self, work_id):
        token = request.headers.get('Authorization')
        result = company_service.find_work_by_id(token, work_id)
        return response(result)

    def delete(self, work_id):
        data = request.get_json()
        account = data.get('account')
        token = request.headers.get('Authorization')
        result = company_service.delete_work_by_id(token, account, work_id)
        return response(result)


@company.route('/session')
class Resume(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        account = request.args.get('account')
        work_id = request.args.get("work_id")
        page = request.args.get('page') or 1
        limit = request.args.get('limit') or 10
        result = company_service.find_session(token, account, work_id,
                                              page, limit)
        return response(result)

    def post(self):
        data = request.get_json()
        token = request.headers.get("Authorization")
        student = data.get('student')
        company_id = data.get("company_id")
        company_name = data.get("company_name")
        work_id = data.get("work_id")
        work_name = data.get("work_name")
        status = data.get('status') or 0
        place = data.get('place')
        date = data.get('date')
        result = company_service.create_session(token, student, company_id,
                                                company_name, work_id,
                                                work_name, status,
                                                place, date)
        return response(result)

    def put(self):
        data = request.get_json()
        token = request.headers.get("Authorization")
        account = data.get("account")
        session_id = data.get('session_id')
        status = data.get('status') or 0
        place = data.get('place')
        date = data.get('date')
        result = company_service.push_session(token, account, session_id,
                                              status, place, date)
        return response(result)

    def delete(self):
        """
        删除学生收到的邀请
        :return:
        """
        token = request.headers.get('Authorization')
        data = request.get_json()
        account = data.get("account")
        session_id = data.get("session_id")
        result = company_service.delete_session(token, account, session_id)
        return response(result)


@company.route('/resume')
class Resume(Resource):
    def get(self):
        token = request.headers.get("Authorization")
        name = request.args.get("name")
        major = request.args.get("major")
        education = request.args.get("education")
        city = request.args.get("city")
        work = request.args.get("work")
        page = request.args.get('page') or 1
        limit = request.args.get('limit') or 10
        result = company_service.get_resume(token, name, major, education,
                                            city, work, page, limit)
        return response(result)


@company.route('/session/<session_id>')
class ResumeById(Resource):
    def get(self, session_id):
        token = request.headers.get("Authorization")
        account = request.args.get('account')
        result = company_service.find_resume_details(token, account, session_id)
        return response(result)

    def put(self, session_id):
        data = request.get_json()
        token = request.headers.get("Authorization")
        account = data.get('account')
        result = company_service.read_resume(token, account, session_id)
        return response(result)
