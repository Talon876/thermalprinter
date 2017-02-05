import os
import json
from flask import render_template, flash, redirect, request, url_for, g
from flask_login import login_user, logout_user, current_user, login_required
import datetime as dt

from app import app, db, lm, blockchain, convert_btc_to_credits
from .auth import OAuthSignIn
from .models import User, BitcoinAddress, BitcoinTransaction, CreditTransaction

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

@app.route('/profile')
@login_required
def profile():
    txns = g.user.btc_address.txns.filter_by(credit_txn=None).all() if g.user.btc_address else []
    return render_template('profile.html', title='Your Profile', txns=txns)

@app.route('/setup-bitcoin', methods=['POST'])
@login_required
def setup_bitcoin():
    if g.user.btc_address:
        flash('You already have a bitcoin address setup.')
    else:
        label = '{}:{}'.format(g.user.social_id, os.urandom(3).encode('hex'))
        new_addr = blockchain.generate_address(label)
        app.logger.info('Generated address {} for user {}'.format(new_addr, g.user))
        if new_addr == "" or new_addr is None:
            flash('Failed to generate a bitcoin address. Please try again in a few minutes.')
        else:
            btc_addr = BitcoinAddress(address=new_addr, label=label, owner=g.user)
            db.session.add(btc_addr)
            db.session.commit()
    return redirect(url_for('profile'))

@login_required
@app.route('/bitcoin/transaction-refresh', methods=['POST'])
def refresh_transactions():
    if not g.user.btc_address:
        flash('You must obtain a bitcoin address first')
    else:
        address_info = blockchain.address_info(g.user.btc_address.address)
        txns = [{
                'txn_hash': txn['hash'],
                'block_height': txn.get('block_height', 0),
                'timestamp': dt.datetime.utcfromtimestamp(txn['time']),
                'amount': sum([t['value'] for t in txn['out']]),
            } for txn in address_info['txs'] if txn.get('block_height', 0) != 0]

        txn_hashes = set([t['txn_hash'] for t in txns])
        known_hashes = set([t[0] for t in BitcoinTransaction.query.with_entities(BitcoinTransaction.txn_hash).all()])
        new_hashes = txn_hashes - known_hashes
        app.logger.info('Found {} new hashes for address {}'.format(', '.join(new_hashes), g.user.btc_address.address))
        if len(new_hashes) > 0:
            txns = [BitcoinTransaction(address=g.user.btc_address, **t) for t in txns if t['txn_hash'] in new_hashes]
            for txn in txns:
                db.session.add(txn)
            db.session.commit()
            flash('Imported {} new transaction(s)'.format(len(new_hashes)))
        else:
            flash('No new transactions found. Try again in a few minutes if you just sent some bitcoins.')
    return redirect(url_for('profile'))

@app.route('/convert/bitcoin/<txnhash>', methods=['POST'])
@login_required
def bitcoin_to_credits(txnhash):
    bitcoin_txn = BitcoinTransaction.query.filter_by(txn_hash=txnhash).first()
    if bitcoin_txn is None:
        flash('That transaction does not exist')
        return redirect(url_for('profile'))
    if bitcoin_txn.address != g.user.btc_address:
        app.logger.warn('Somebody tried to convert a transaction that wasn\'t their own')
        flash('That transaction does not exist')
        return redirect(url_for('profile'))
    if bitcoin_txn.credit_txn is not None:
        flash('This transaction has already been processed')
        return redirect(url_for('profile'))

    bitcoin_amt = bitcoin_txn.bitcoin_amount
    credit_amt = int(convert_btc_to_credits(bitcoin_amt))

    credit_txn = CreditTransaction(credit_amount=credit_amt, is_debit=False, pending=False, owner=g.user)
    bitcoin_txn.credit_txn = credit_txn
    g.user.credits += credit_amt
    db.session.add(g.user)
    db.session.add(bitcoin_txn)
    db.session.add(credit_txn)
    db.session.commit()
    flash('You have received {} credits!'.format(credit_amt))
    return redirect(url_for('profile'))

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

