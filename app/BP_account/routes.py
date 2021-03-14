from app.BP_account import BP_account
from flask.templating import render_template
from flask_login import login_required
from flask.helpers import url_for
from flask_login import login_user, logout_user, current_user
from flask import redirect, url_for, flash, render_template, request, jsonify
from markupsafe import Markup
from app import db, encryptor, mail
import app.utils as utils
from app.models import User

from app.BP_account.forms import UpdateForm, PasswordForm




@BP_account.route("/account-info" , methods=['GET' , 'POST'])
@login_required
def account_info():
    update_form_prefix = "updateForm"
    change_pwd_prefix = "pwdForm"
    form = UpdateForm(prefix=update_form_prefix)
    form1 = PasswordForm(prefix=change_pwd_prefix)
    dp_file = url_for('static', filename='images/user-dp/' + current_user.dp_file)
    if request.method == "POST" and request.form["form"] == "info":
        if form.validate_on_submit():
            utils.update_user(form.data)
            content = [f"Success", f"Your details are updated."]
            flash(content, category="success")
            return redirect(url_for("BP_account.account_info"))
    elif request.method == "POST" and request.form["form"] == "pwd":
        if form1.validate_on_submit():
            utils.change_password(form1.new_password.data)
            content = [f"Success", f"Your assword is updated."]
            flash(content, category="success")
            return redirect(url_for("BP_account.account_info"))   
    return render_template("acchome.html", title="My Account", dp_file = dp_file, updateForm=form , pwdForm=form1)

    

   
