from flask import Flask, render_template, request, redirect, url_for,session,abort
from google_auth_oauthlib.flow import Flow
import pathlib

import os
from pathlib import Path

app = Flask('__name__')
app.secret_key = 'secret key'
GOOGLE_CLIENT_ID = "625444172244-4cnk1t6urql2mblfq359kdpj963sn8ui.apps.googleusercontent.com"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client_secret_file = os.path.join(Path(__file__).parent, 'client_secrete.json')


flow = Flow.from_client_secrets_file(client_secrets_file=client_secret_file,scopes=['https://www.googleapis.com/auth/userinfo.profile','openid', 'https://www.googleapis.com/auth/userinfo.email'],redirect_uri='http://127.0.0.1:5000/callback')

def login_required(function):
  def wrapper(*args, **kwargs):
    if "google_id" not in session:
      return abort(401)
    else:
      return function()
  return wrapper




@app.route('/login')
def login():
  authorization_url, state = flow.authorization_url()
  session["state"] = state
  return redirect(authorization_url)
  


@app.route('/callback')
def callback():
  flow.fetch_token(authorization_response=request.url)
  if not session["state"] == request.args["state"]:
    abort(500)
  credentials = flow.credentials
  request_session = requests.session()
  cached_session = cachecontrol.CacheControl(request_session)
  token_request = google.auth.transport.requests.Request(session=cached_session)

  id_info = id_token.verify_oauth2_token(id_token=credentials._id_token,
                                         request=token_request,
                                         audience=GOOGLE_CLIENT_ID)
  session["google_id"] = id_info.get("sub")
  session["name"] = id_info.get("name")
  return redirect('/protected')

@app.route('/logout')
def logout():
  session.clear()
  return redirect("/")
  

@app.route('/')
def index():
  return "hello world <a href='/login' ><button>Login</button></a>" 


@app.route('/protected')
# @login_required
def protected():
  return "<h1> protected</h1> <a href='/logout' ><button>Logout</button></a> "

if __name__ == '__main__':
  app.run(debug=True)
