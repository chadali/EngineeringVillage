from app import app, google, sheet, db
from .models import User
from .forms import LoginForm
from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from flask_login import login_user , logout_user , current_user , login_required


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    if me.data['hd'] == 'ncsu.edu':
        try:
            user = User.query.filter_by(email=me.data['email']).first()
        except:
            user = None
            pass
        if user is None:
            try:
                list_of_hashes = sheet.get_all_records()
                for person in list_of_hashes:
                    if person['Unity ID'] == me.data['email'].split('@')[0]:
                        totalPoints = person['Total Points']
                        break
            except:
                return "Google sign in worked. Could not get sheet values"
            newAccount = User(email=me.data['email'], first_name=me.data['given_name'] , last_name=me.data['family_name'], points=totalPoints, image=me.data['picture'])
            db.session.add(newAccount)
            db.session.commit()
            login_user(newAccount, remember=True)
        else:
            login_user(user, remember=True)
        session.pop('google_token', None)
    else:
        session.pop('google_token', None)
        return "<h1> Log in with NCSU email </h1>"
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')