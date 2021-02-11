from app.BP_account import BP_account
from flask.templating import render_template

@BP_account.route("/account-info")
def account_info():
    return render_template("acchome.html")
    
    
