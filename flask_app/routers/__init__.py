from flask import jsonify, make_response
from flask_app import MESSAGE_DICT


def response(result):
    if result.get("message") == MESSAGE_DICT.SUCCESS:
        return make_response(jsonify(result), 200)
    else:
        return make_response(jsonify(result), 400)
