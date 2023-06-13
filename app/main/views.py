from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, flash, request
from flask_login import login_required, current_user

from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..email import send_email
from ..models import User, Role, Permission, Post
from app.decorators import admin_required, permission_required


# Маршруты и представления
@main.route("/", methods=["GET", "POST"])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for(".index"))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template("main/index.html", form=form, posts=posts, pagination=pagination)


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
    page = request.args.get("page", 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config["FLASKY_POSTS_PER_PAGE"],
        error_out=False)
    posts = pagination.items
    return render_template("main/user.html", user=user, posts=posts, pagination=pagination)


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
