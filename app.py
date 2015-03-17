from flask import Flask, render_template, url_for, flash, request, redirect, jsonify, session
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_oauth import OAuth
from dropbox.client import DropboxClient
import os
import getpass

app = Flask(__name__)

DEBUG = True
SECRET_KEY = "sheep"

app.debug = DEBUG
app.secret_key = SECRET_KEY

# changing jinja delimiters so won't interfere with AngularJS
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

if (getpass.getuser() == "andrew"):
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://username:password@localhost/test"
else:
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] # Comment out when working on local
  pass
db = SQLAlchemy(app)

# importing models dependent on db
from models import *

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  return User.query.get(userid)

@app.route('/')
def index():
  return render_template('index.html')

# implementing Facebook OAuth login
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

@app.route('/login')
def facebook_login():
  return facebook.authorize(callback=url_for('facebook_authorized',
         next=request.args.get('next') or request.referrer or None,
         _external=True))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
  next_url = request.args.get('next') or url_for('index')
  if resp is None:
    return 'Access denied: reason=%s error=%s' % (
           request.args['error_reason'],
           request.args['error_description'])
  session['oauth_token'] = (resp['access_token'], '')
  user_data = facebook.get('/me').data
  user = User.query.filter(User.fb_id == user_data['id']).first()
  if user is None:
    new_user = User(fb_id=user_data['id'], first_name=user_data['first_name'], last_name=user_data['last_name'])
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
  else:
    login_user(user)
  return redirect(next_url)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_oauth_token():
  return session.get('oauth_token')

# implementing third-party dropbox storage for user files
DROPBOX_ACCESS_TOKEN = "rL0DF7AV9PAAAAAAAAAABk4ZmCRtES_UH33Ty8nV7Za4n22LDFUwJcA7h3do2OGe"
dropbox_client = DropboxClient(DROPBOX_ACCESS_TOKEN)

@app.route('/me')
@login_required
def show_me():
  return render_template('my_profile.html',
                         user=current_user)

@app.route('/me/upload', methods=['POST'])
@login_required
def me_upload():
  uploaded_file = request.files.get("file_data")
  filename = uploaded_file.filename
  dropbox_response = dropbox_client.put_file(filename, uploaded_file)
  dropbox_filepath = dropbox_response['path']
  return jsonify(error="Flask received file. Located at Dropbox filepath: " + str(dropbox_filepath))

@app.route('/<fb_id>')
def show_user(fb_id):
  user = User.query.filter_by(fb_id=fb_id).first()
  if user is None:
    flash('User %s not found.' % nickname)
    return redirect(url_for('index'))
  else:
    return render_template('user_profile.html',
                           user=user)

if __name__ == "__main__":
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
