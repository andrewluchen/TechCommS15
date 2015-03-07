from flask import Flask, render_template, request, url_for, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_oauth import OAuth
import os

app = Flask(__name__)

DEBUG = False
SECRET_KEY = "sheep"

app.debug = DEBUG
app.secret_key = SECRET_KEY

# Changing jinja delimiters so won't interfere with AngularJS
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

db = SQLAlchemy(app)

# models depends on db
from models import *

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  return User.query.get(userid)

FACEBOOK_APP_ID = "928787610474878"
FACEBOOK_APP_SECRET = "b8287fd361cf054c37a5d30b6122237b"

oauth = OAuth()
facebook = oauth.remote_app('facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': 'email'}
)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login')
def facebook_login():
  return facebook.authorize(callback=url_for('facebook_authorized',
         next=request.args.get('next') or request.referrer or None,
         _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
           request.args['error_reason'],
           request.args['error_description'])
  session['oauth_token'] = (resp['access_token'], '')
  me = facebook.get('/me')
  user = User.query.filter(User.fb_id == me['id']).first()
  if user is None:
    new_user = User(first_name=me['first_name'], last_name=me['last_name'])
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
  else:
    login_user(user)
  return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
  return session.get('oauth_token')

@app.route('/me')
def show_userprofile():
  return "0"

@app.route('/user/<fb_id>')
def show_users():
  return "0"

if __name__ == "__main__":
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
