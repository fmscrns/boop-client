from flask import session, redirect, url_for
from functools import wraps


def session_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "booped_in" in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("gateway.signin"))
    
    return wrap

def no_session_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "booped_in" in session:
            return redirect(url_for("home.feed"))
        else:
            return f(*args, **kwargs)

    return wrap