from app.BP_admin import BP_admin
from app.models import User
from app.decorators import admin_required
from flask.templating import render_template
from flask_login import login_required

@BP_admin.route("/admin")
@login_required
@admin_required
def home():
    return render_template("admin.layout.html", title="Admin Home")