from flask import render_template, flash, redirect, request, url_for, g
import datetime as dt

from app import app, db
from .auth import OAuthSignIn
from .models import User

@app.before_request
def before_request():
    g.user = None

@app.route('/')
def index():
    return render_template('index.html',
            title='Home')

@app.route('/login')
def login():
    providers = [
        { 'name': 'twitch', 'button_img': 'https://i.imgur.com/f9H7QoX.png' }
    ]
    return render_template('login.html', title='Login', providers=providers)

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
        user = User(social_id=social_id)
        app.logger.info('Adding user {} to database'.format(social_id))
        db.session.add(user)
        db.session.commit()
    app.logger.info('Authorized {}'.format(user))
    return redirect(url_for('index'))

