from app.BP_account import BP_account
from flask.templating import render_template
from flask_login import login_required

@BP_account.route("/account-info")
@login_required
def account_info():
    return render_template("acchome.html")
    

        
