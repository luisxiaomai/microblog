from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask_login import current_user
from . import main
from .forms import NameForm, EditProfileForm,EditProfileAdminForm
from .. import db, photos
from ..models import User,Role
from ..email import send_email

from ..decorators import admin_required, permission_required
from ..models import Permission
from flask_login import login_required


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


@main.route('/admin', methods=["GET","POST"])
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"

@main.route("/user/<username>",methods=["GET","POST"])
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template("user.html", user=user)

@main.route("/editProfile",methods=["GET","POST"])
@login_required
def edit_user():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        if form.photo.data:
            current_user.image_filename = photos.save(form.photo.data,name="user/" + current_user.name + ".")
            current_user.image_url = photos.url(current_user.image_filename)
        db.session.add(current_user)
        return redirect(url_for("main.user",username=current_user.username))
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me    
    return render_template("editProfile.html", form=form, image_url=current_user.image_url)

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
        user.location = form.location.data
        user.about_me = form.about_me.data
        if form.photo.data:
            user.image_filename = photos.save(form.photo.data, name="user/" + user.username+".")
            user.image_url = photos.url(current_user.image_filename)
        db.session.add(user)
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('editProfile.html', form=form, user=user,image_url=user.image_url)
