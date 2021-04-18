from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from .models import User
from flask_login import login_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Username doesn't exist")
        return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    username = request.form.get('username')

    user = User.query.filter_by(username=username).first() # Should check if username exists

    if user:
        flash('Username already exists')
        return redirect(url_for('auth.signup'))

    new_user = User(username=username) # This is where the sha256 hash for pass would go

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
