import json
import requests
from web import db
import web.models as m
from web import host_ip
from web.forms import NewUserForm
from requests.auth import HTTPBasicAuth
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
import platform

null = 'null'

def clear_user_space():
    users = m.User.query.all()
    for user in users:
        URI = "http://{}:5002/User/{}/exists".format(host_ip, user.username)
        request = requests.get(URI)
        requestJSON = json.loads(request.text)
        if not requestJSON['data'][0]['exists']:
            db.session.delete(user)
    db.session.commit()


def register_new_user(username, password, firstname, lastname,
                      email, middlename, submit):
    package = {"username": username, "password": password,
               "firstname": firstname, "lastname": lastname, "email":email,
               "platform": platform.platform(), "middlename": middlename}
    URI = "http://{}:5002/User/register/".format(host_ip)
    request = requests.post(URI, data=package)

def check_first_time_setup():
    request = requests.get("http://{}:5002/User/number".format(host_ip))
    print(request.text)
    requestJSON = json.loads(request.text)
    return requestJSON['data'][0]['number'] == 0

def run_first_time_setup():
    return render_template('setup.html', **locals())

def run_normal_login():
    URI = 'http://{}:5002/Books'.format(host_ip)
    if current_user.is_authenticated:
        print('logged in')
        response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
        if response.text != "Unauthorized Access":
            json_data = json.loads(response.text)
            books = json_data['data']
            numBooks = len(books)
            titles = [x['title'] for x in books]
            descs = [x['description'].replace('\\n', '<br>') for x in books]
            authors = [x['Authors'] for x in books]
            narrators = [x['Narrators'] for x in books]

            info = {"titles": titles, "descs": descs, "authors": authors,
                    "narrators": narrators}
            forceLogin = False
        else:
            logout_user()
            info = {}
            forceLogin = True
    else:
        print('not logged in')
        info = {}
        forceLogin = True

    return render_template('index.html', **locals())
