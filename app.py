from flask import Flask, render_template, request, redirect, url_for,session,abort

app = Flask('__name__')
app.secret_key = 'secret key'

def login_required(function):
  def wrapper(*args, **kwargs):
    if "google_id" not in session:
      return abort(401)
    else:
      return function()
  return wrapper




@app.route('/login')
def login():
  session['googe_id'] = "test"
  return redirect("/protected")
  


@app.route('/callback')
def callback():
  pass

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
  app.run(host='0.0.0.0', port=8080,debug=True)
