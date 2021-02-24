from threading import Thread
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


# Creates background thread using decorator '@threader'
def threader(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.admin:
            return f(*args, **kwargs)
        else:
            content = [f"Unauthorized", f"You don't have access to view this page."]
            flash(content, category="danger")
            return redirect(url_for("BP_home.home"))

    return wrap
