from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email

@main.route("/", methods=["GET","POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        queryUser=User.query.filter_by(username=form.name.data).first()
        if queryUser is None:
            user=User(username=form.name.data)
            db.session.add(user)
            send_email(form.name.data,"New user", "mail/new_user", user=user)
        session["UserExisted"]=form.name.data
        return redirect(url_for("main.index"))
    return render_template("index.html", form=form,known=session.get("UserExisted",False))
