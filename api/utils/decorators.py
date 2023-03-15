from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify, abort
from copy import deepcopy

def student_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "student" in claims:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Students users only!"), 403

        return decorator

    return wrapper

def teacher_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if "teacher" in claims:
                return fn(*args, **kwargs)
            else:
                return jsonify(msg="Teacher users only!"), 403

        return decorator

    return wrapper

def alt_response(
        status_code,
        response=None,
    ):
    if response is not None:
        resp_doc = response

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        x = wrapper
        wrapper._apidoc = deepcopy(getattr(wrapper, "_apidoc", {}))
        wrapper._apidoc.setdefault("response", {}).setdefault("responses", {})[
            status_code
        ] = resp_doc
        return wrapper
    return decorator