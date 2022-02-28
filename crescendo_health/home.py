from ast import Try
from cgitb import reset
from curses.ascii import US
import email
import json
import requests
from flask import Flask,redirect, request, session,url_for,render_template
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
load_dotenv()
import os
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = os.urandom(24)

oauth = OAuth(app)


app.config["GITHUB_CLIENT_ID"] = os.getenv("GITHUB_CLIENT_ID")
app.config["GITHUB_CLIENT_SECRET"]= os.getenv("GITHUB_CLIENT_SECRET")
user = {}
res = []

github = oauth.register(
    name = "github",
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret=app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = "https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params = None,
    api_base_url = "https://api.github.com/",
    client_kwargs = {'scope':'user:email'}
)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login/github")
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for("github_authorize",_external="True")
    return github.authorize_redirect(redirect_uri)


@app.route("/login/github/authorize", methods=['GET', 'POST'])
def github_authorize():
    github = oauth.create_client("github")
    token = github.authorize_access_token()
    resp = github.get("user").json()
    user["email"] = resp["html_url"]
    user["username"] = resp["login"]
    session["username"]= resp["login"]
    user["access_token"] = token["access_token"]
    user["activation_code"] = request.args.get('code')
    user["avatar"] = resp["avatar_url"]
    repo =  requests.get(f"https://api.github.com/users/{user['username']}/repos")
    data = json.loads(repo.text)
    try:
        for el in data:
            res.append([el["name"],el["svn_url"]])
        return redirect(url_for("activation_code_post"))
    except NameError:
        return "Something went wrong with getting the repo"
    except:
        return "Something else went wrong"


@app.route('/login/github/authorize/code', methods=['GET','POST'])
def activation_code_post():
    if request.method == 'GET':
        return render_template("activate.html")
    if request.method == 'POST':
        input_code = request.form['text']
        if input_code == user["activation_code"]:
            return render_template("user_repo.html",data=res,name=user["username"])
        else:
            return render_template("activate.html", data="Activation code incorrect")

 
if __name__ == "__main__":
    app.debug = True
    app.run()

