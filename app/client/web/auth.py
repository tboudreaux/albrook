import json
import requests
from web import db
from web import app
import web.models as m
from web import host_ip
from datetime import datetime
from datetime import timedelta
from requests.auth import HTTPBasicAuth

null = 'null'

def UserInDB(username):
    user = m.User.query.filter_by(username=username).first()
    if user:
        return True
    else:
        return False

def get_user_token(user, psw, token=None):
    if token:
        authID = token
    else:
        authID = user
    request = requests.get('http://{}:5002/User/{}/token'.format(host_ip, user),
                            auth=HTTPBasicAuth(authID, psw))
    try:
        requestJSON = json.loads(request.text)
        return requestJSON['token']
    except ValueError:
        return 'NO_TOKEN'

def get_user_info(user):
    URI = 'http://{}:5002/User/{}/info'.format(host_ip, user.username)
    request = requests.get(URI, auth=HTTPBasicAuth(user.token, 'null'))
    return json.loads(request.text)

def load_user_info(user):
    userInfo = get_user_info(user)
    user.id = userInfo['id']

def addUserToLocalDB(username, psw, f=False):
    if not UserInDB(username):
        print("username and password: ", username, psw)
        token = get_user_token(username, psw)
        if token != 'NO_TOKEN':
            newUser = m.User()
            newUser.username = username
            newUser.token = token
            newUser.tokenLeaseStart = datetime.now()
            load_user_info(newUser)
            db.session.add(newUser)
            db.session.commit()
            return True
    else:
        return renewUserToken(username, psw)
    return False


def renewUserToken(username, psw):
    if UserInDB(username):
        user = m.User.query.filter_by(username=username).first()
        if datetime.now() < user.tokenLeaseStart + timedelta(seconds=550):
            # Renew token with token if previous token lease is valid
            # does not need password
            token = get_user_token(user.username, '', token=user.token)
            if token != 'NO_TOKEN':
                user.token = token
                user.tokenLeaseStart = datetime.now()
                db.session.commit()
                return True
        else:
            # renew token with username and password, if previous token
            # lease is no longer valid
            token = get_user_token(username, psw)
            if token != 'NO_TOKEN':
                user.token = token
                user.tokenLeaseStart = datetime.now()
                db.session.commit()
                return True
    return False
