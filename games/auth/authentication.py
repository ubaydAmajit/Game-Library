from functools import wraps

from flask import Blueprint, render_template, url_for, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from password_validator import PasswordValidator

from games.auth import services
import games.adapters.repository as repo

auth_blueprint = Blueprint(
    'auth_bp', __name__, url_prefix='/auth')


@auth_blueprint.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    username_not_unique = None
    print(form.errors)
    if form.validate_on_submit():
        try:
            services.new_user(form.username.data, form.password.data, repo.repo_instance)
            return redirect(url_for('auth_bp.login'))
        except services.NonUniqueUsernameException:
            username_not_unique = "This Username Is Already Taken"
    return render_template("auth/credentials.html",
                           title="Register", auth_error_message=username_not_unique, form=form)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    credential_error = None
    if form.validate_on_submit():
        try:
            user = services.get_user(form.username.data, repo.repo_instance)
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            session.clear()
            session["username"] = user["username"]
            return redirect(url_for("home_bp.home"))
        except services.UnknownUserException:
            credential_error = "Invalid Credentials"
        except services.AuthenticationException:
            credential_error = "Invalid Credentials"
    return render_template("auth/credentials.html",
                           title="Login", auth_error_message=credential_error, form=form)


@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home_bp.home"))


def login_required(f):
    @wraps(f)
    def wrapper(**kwargs):
        if "username" not in session:
            return redirect(url_for("auth_bp.login"))
        return f(**kwargs)
    return wrapper


class LengthValidation:
    def __init__(self, message=None):
        self.min_length = 10
        if not message:
            message = f"Your password should contain at least {self.min_length} characters"
        self.message = message

    def __call__(self, form, field):
        validator = PasswordValidator().min(self.min_length)
        valid = validator.validate(field.data)
        if not valid:
            raise ValidationError(self.message)


class CharacterValidation:
    def __init__(self, message=None):
        if not message:
            message = "Your password should contain lowercase and uppercase letters, numbers, and no spaces"
        self.message = message

    def __call__(self, form, field):
        validator = PasswordValidator() \
            .has().digits() \
            .has().uppercase() \
            .has().lowercase() \
            .has().no().spaces()
        valid = validator.validate(field.data)
        if not valid:
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField("Username", [
        DataRequired(message="Please enter your Username"),
        Length(message="Your Username needs to be longer", min=3)
    ])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        LengthValidation(),
        CharacterValidation()
    ], )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')
