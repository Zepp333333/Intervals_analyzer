from flask import Flask, render_template, flash, redirect, url_for, request
import logger
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from requests import Request
from strava_ops import get_access_token


log = logger.logger
# log.error("Front started")


@app.route("/")
@app.route('/index')
def index():
    return render_template('index.html', link="https://www.strava.com/oauth/authorize?client_id=50434&redirect_uri=http://localhost:5000/StravaAuthReturn&response_type=code&scope=activity:read_all")

#todo refactor variable names to align to convention



# if __name__ == "__main__":
#     app.run()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]

    # TODO: parametrize URLs building (put the building routine into Strava_ops

    auth_url = "https://www.strava.com/oauth/authorize"
    param = {'client_id': '50434',
             'redirect_uri': ('http://localhost:5000/user/' + str(username) + '/StravaAuthReturn'),
             'response_type': 'code',
             'scope': 'activity:read_all'}
    req = Request('GET', auth_url, params=param).prepare().url
    return render_template(
        'user.html', user=user,
        posts=posts,
        strava_auth_link=str(req))

# if __name__ == '__main__':
#     main()

@app.route('/user/<username>/StravaAuthReturn')
def state(username):
    strava_auth_code = request.args.get('code', default=None, type=str)
    strava_auth_scope = request.args.get('scope', default=None, type=str)
    user = User.query.filter_by(username=username).first_or_404()
    strava_athlete_json = get_access_token(None, strava_auth_code)
    user.set_strava_id(strava_athlete_json['athlete']['id'])
    db.session.add(user)
    db.session.commit()
    user.add_strava_athlete_json(strava_athlete_json)
    db.session.add(user)
    db.session.commit()
    return render_template('StravaAuthReturn.html', code=strava_auth_code, username=username, atuth_json=strava_athlete_json)
