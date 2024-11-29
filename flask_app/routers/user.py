# -------------------------------------导包--------------------------------------
from flask import request
from flask_restx import Namespace, Resource

from flask_app import MESSAGE_DICT
from flask_app.routers import response
from flask_app.services import user_service

# -------------------------------------常量--------------------------------------
user = Namespace("user", path='/user', description='用户管理')


# -------------------------------------代码--------------------------------------
@user.route('/login')
class Login(Resource):
    @user.doc("获取用户信息")
    def get(self):
        token = request.headers.get("Authorization")
        result = user_service.get_token_info(token)
        if result:
            return {"message": MESSAGE_DICT.SUCCESS, "data": result}
        return {"message": MESSAGE_DICT.NOT_FOUND.format("用户信息"), "data": []}

    @user.doc("登录")
    def post(self):
        data = request.get_json()
        account = data.get('account')
        password = data.get('password')
        addr = request.remote_addr
        result = user_service.login(account, password, addr)
        return response(result)

    @user.doc('修改密码')
    def put(self):
        token = request.headers.get('Authorization')
        data = request.get_json()
        account = data.get('account')
        old_pass = data.get('old_pass')
        password = data.get('password')
        check_passwd = data.get('check_pass')
        result = user_service.modify_pass(account, old_pass,
                                          password, check_passwd, token)
        return response(result)


@user.route('/account')
class Account(Resource):

    @user.doc("获取用户信息")
    def get(self):
        token = request.headers.get("Authorization")
        account = request.args.get("account")
        result = user_service.get_user_info(token, account)
        return response(result)

    @user.doc("注册")
    def post(self):
        data = request.get_json()
        account = data.get("account")
        username = data.get('username')
        password = data.get('password')
        check_passwd = data.get('check_passwd')
        sex = data.get("sex")
        image = data.get("image") or 'imgs/default.jpg'
        email = data.get('email')
        phone = data.get('phone')
        introduce = data.get('introduce') or 'Ta的自我介绍正在路上...'
        profession = data.get('profession')
        is_admin = data.get('is_admin') or False
        result = user_service.register(account, username, password,
                                       check_passwd, sex, image, phone, email,
                                       introduce, profession, is_admin)
        return response(result)

    @user.doc("修改信息")
    def put(self):
        data = request.get_json()
        token = request.headers.get('Authorization')
        account = data.get('account')
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        image = data.get("image") or '/assets/img/default.jpg'
        profession = data.get('profession')
        introduce = data.get('introduce')
        member_level = data.get('member_level') or None
        is_admin = data.get("is_admin") or False
        result = user_service.modify_info(account, username, email, phone, image,
                                          profession, introduce, member_level, is_admin, token)
        return response(result)


@user.route("/image")
class UserImage(Resource):

    @user.doc("获取用户头像")
    def get(self):
        token = request.headers.get('Authorization')
        username = request.args.get("username")
        result = user_service.get_image(username, token)
        return response(result)

    @user.doc("上传图片")
    def post(self):
        image = request.files.get('file')
        result = user_service.upload_image(image)
        return response(result)


@user.route("/message")
class Message(Resource):
    def get(self):
        token = request.headers.get('Authorization')
        account = request.args.get("account")
        result = user_service.count_message(token, account)
        return response(result)
