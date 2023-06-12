from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash
from flask_login import login_required, current_user

from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm
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
        "main/index.html", name=session.get("name"), form=form,
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


@main.route("/user/<username>", methods=["GET"])
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("main/user.html", user=user)


@main.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user_profile', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', form=form)


# Редактирование профилей других пользователей от администратора
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user_profile', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('main/edit_profile.html', form=form, user=user)
