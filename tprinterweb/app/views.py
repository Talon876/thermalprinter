from flask import render_template, flash, redirect, request, url_for, g
import datetime as dt

from app import app, db
from .auth import OAuthSignIn

@app.route('/')
def index():
    return render_template('index.html',
            title='Home')

