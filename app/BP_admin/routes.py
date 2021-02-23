from app.BP_admin import BP_admin
from app.models import User
from app.decorators import admin_required
from flask.templating import render_template
from flask_login import login_required

@BP_admin.route("/admin/home")
@login_required
@admin_required
def home():
    return render_template("admin-home.html", title="Admin Home")