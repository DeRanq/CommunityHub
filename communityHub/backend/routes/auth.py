from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from ..models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    return redirect(url_for('forum.uebersicht'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('forum.uebersicht'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm', '')

        if not username or not email or not password:
            flash('Alle Felder sind Pflichtfelder.', 'danger')
        elif password != confirm:
            flash('Passwörter stimmen nicht überein.', 'danger')
        elif len(password) < 6:
            flash('Passwort muss mindestens 6 Zeichen lang sein.', 'danger')
        elif User.query.filter_by(username=username).first():
            flash('Benutzername bereits vergeben.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('E-Mail bereits registriert.', 'danger')
        else:
            user = User(
                username=username,
                email=email,
                password=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            flash('Registrierung erfolgreich! Bitte melde dich an.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('forum.uebersicht'))

    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Willkommen zurück, {user.username}!', 'success')
            return redirect(next_page or url_for('forum.uebersicht'))
        else:
            flash('E-Mail oder Passwort falsch.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Du wurdest abgemeldet.', 'info')
    return redirect(url_for('auth.login'))
