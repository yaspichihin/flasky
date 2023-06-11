from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from flask_login import login_required

from . import main
from .forms import NameForm
from .. import db
from ..email import send_email
from ..models import User, Role, Permission
from app.decorators import admin_required, permission_required


# Маршруты и представления
@main.route("/", methods=["GET", "POST"])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user: User = User.query.filter_by(username=form.name.data).first()
        if not user:
            user: User = User(username=form.name.data)
            db.session.add(user)
            session["known"] = False
            # Отправка почты при новом пользователе в поле
            app = current_app._get_current_object()
            if app.config["MAIL_SENDER"]:
                send_email(
                    app.config["MAIL_RECEIVER"], "New User",
                    "main/email/new_user",  user=user
                )
        else:
            session["known"] = True
        session["name"] = form.name.data
        # Очистка формы
        form.name.data = ""
        return redirect(url_for(".index"))
    return render_template(
        "index.html", name=session.get("name"), form=form,
        current_time=datetime.utcnow(), known=session.get("known", False),
    )


@main.route("/smoke", methods=["GET"])
def smoke():
    return {"message": "smoke"}, 200


# Маршрут только для администраторов
@main.route("/admin", methods=["GET"])
@login_required
@admin_required
def for_admins_only():
    return "Route only for administrators"


# Маршрут только для администраторов и модераторов
@main.route("/moderator", methods=["GET"])
@login_required
@permission_required(Permission.MODERATE)
def for_admins_and_moderators_only():
    return "Route only for moderators"


@main.route("/data", methods=["GET"])
def data():
    Role.insert_roles()
    return {"message": "smoke"}, 200
