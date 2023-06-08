from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..email import send_email
from ..models import User


# Маршруты и представления
@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        usr: User = User.query.filter_by(username=form.name.data).first()
        if usr is None:
            usr: User = User(username=form.name.data)
            db.session.add(usr)
            session["known"] = False
        else:
            session["known"] = True
        session["name"] = form.name.data
        # Очистка формы
        form.name.data = ""
        return redirect(url_for(".index"))
    return render_template("index.html",
                           name=session.get("name"),
                           form=form,
                           current_time=datetime.utcnow(),
                           known=session.get("known", False),
                           )


@main.route("/email", methods=["GET", "POST"])
def email():
    send_email("yaspichihin@yandex.ru", "yarjust@yandex.ru", "New User",
               "auth/email/new_user", user="yar")
    return "sent"
