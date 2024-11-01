# -*- coding: utf-8 -*-
from flask import url_for
from flask_caching import Cache
from flask_restx import Api
from configs.config import current_config
from flask_app.databases import db
from configs.application import app
from flask_app.models import user_model
from flask_app.routers.user import user
cache = Cache()


class MyApi(Api):
    @property
    def specs_url(self):
        scheme = 'http'
        return url_for(self.endpoint('specs'), _external=True, _scheme=scheme)


auth = {
    "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

api = MyApi(
    title="告警服务接口文档",
    version="3.0",
    description="告警服务",
    doc="/docs/",
    security=["Authorization"],
    authorizations=auth
)


def create_app(app):
    app.config.from_object(current_config)
    app.config["PROPAGATE_EXCEPTIONS"] = False
    cache.init_app(app)
    api.init_app(app)
    api.add_namespace(user)
    with app.app_context():
        db.create_all()
    return app


app = create_app(app)
