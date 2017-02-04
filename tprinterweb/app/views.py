from flask import render_template, flash, redirect, request, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
import datetime as dt

from app import app, db, lm
from .auth import OAuthSignIn
from .models import User

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = dt.datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@lm.user_loader
def load_user(uid):
    app.logger.debug('Loading user {}'.format(uid))
    return User.query.get(int(uid))

@app.route('/')
def index():
    return render_template('index.html',
            title='Home')

@app.route('/login')
def login():
    if g.user is not None and g.user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('index'))
    providers = [
        { 'name': 'twitch', 'button_img': '/static/twitch-login.png'}
    ]
    return render_template('login.html', title='Login', providers=providers)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/authorize/<provider>')
def authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_username = oauth.callback()
    if social_username is None:
        flash('Login failed')
        return redirect(url_for('login'))

    social_id = '{}/{}'.format(provider, social_username)
    user = User.query.filter_by(social_id=social_id).first()
    if user is None:
        user = User(social_id=social_id,
                    nickname=social_username)
        app.logger.info('Adding user {} to database'.format(social_id))
        db.session.add(user)
        db.session.commit()
    app.logger.info('Authorized {}'.format(user))
    user.last_login = dt.datetime.utcnow()
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect(url_for('index'))

