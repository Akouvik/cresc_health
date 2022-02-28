#Crescendo Health

This is the readme file for the crescendo health take home screen

#Getting started

Install docker and run:

docker-compose up

# docker-compose stop

Otherwise, for the standalone web service:

pip install -r requirements.txt
python home.py
Visit Homepage : http://127.0.0.1:5000/
callback UR: http://127.0.0.1:5000/login/github/authorize

SECRET_KEY = "THIS SHOULD BE SECRET"
GITHUB_CLIENT_ID = ""
GITHUB_CLIENT_SECRET= ""
