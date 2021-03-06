from web import app, host_ip
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from web.models import User
import requests
import json
from requests.auth import HTTPBasicAuth
from web.auth import addUserToLocalDB
from web.utils import run_normal_login, run_first_time_setup
from web.utils import check_first_time_setup
from web.utils import register_new_user
import platform
from datetime import datetime, timedelta

null = 'null'

# TODO -> fix the issue where unique constraints are not satisfied
#         in the client user DB (should still manifest)
#         issue should be (i think) due to not syncing the DB proper with
#         the server DB

@app.route('/')
def index():
    if check_first_time_setup():
        return run_first_time_setup()
    else:
        return run_normal_login()

        
@app.route('/Book/id:<book_id>/chapter:<chapter_id>/stream')
@login_required
def TrackStream(book_id, chapter_id):
    return 'http://{}:5002/Book/{}/{}/stream.mp3'.format(host_ip, book_id,
                                                         chapter_id)


@app.route('/Book/id:<book_id>/currentTrack')
@login_required
def CurrentUserTrack(book_id):
    print('Getting Track Info for book {}'.format(book_id))
    URI = 'http://{}:5002/Book/{}/user/{}/track'.format(host_ip, book_id,
                                                        current_user.id)

    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Book/id:<book_id>')
@login_required
def getBookInfo(book_id):
    print('HERE')
    URI = 'http://{}:5002/Book/{}'.format(host_ip, book_id)
    print("URI is: ", URI)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    print('response is: ', response.text);
    return response.text

@app.route('/Books')
@login_required
def getBooks():
    URI = 'http://{}:5002/Books'.format(host_ip)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Books/number')
@login_required
def getNumBooks():
    URI = 'http://{}:5002/TotalBooks'.format(host_ip)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Authors')
@login_required
def getAuthors():
    URI = 'http://{}:5002/Authors'.format(host_ip)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Author/name:<author_name>')
@login_required
def getAuthorInfoName(author_name):
    URI = 'http://{}:5002/Author/name/{}'.format(host_ip, author_name)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Author/<author_id>')
@login_required
def getAuthorInfo(author_id):
    URI = 'http://{}:5002/Author/{}'.format(host_ip, author_id)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Books/author/<book_id>')
@login_required
def getBooksByAuthorByBook(book_id):
    URI = "http://{}:5002/Books/author/{}".format(host_ip, book_id)
    request = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return request.text

@app.route('/Author/<author_id>/books')
@login_required
def getAuthorBooks(author_id):
    URI = 'http://{}:5002/Author/{}/books'.format(host_ip, author_id)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text

@app.route('/Book/id:<book_id>/cover/width:<width>/height:<height>')
def getCoverURI(book_id, width, height):
    return 'http://{}:5002/Book/{}/cover/thumbnail:{}:{}'.format(host_ip,
                                                                book_id, width,
                                                                height)


@app.route('/Author/id:<author_id>/portrait/width:<width>/height:<height>')
def getAuthorPortaitURI(author_id, width, height):
    return 'http://{}:5002/Author/{}/portrait/thumbnail:{}:{}'.format(host_ip,
                                                                      author_id,
                                                                      width,
                                                                      height)

@app.route('/Book/id:<book_id>/currentTrack', methods=['POST'])
@login_required
def updateUserBookInfo(book_id):
    jsonPUT = request.get_json()
    URI = 'http://{}:5002/Book/{}/user/{}/track'.format(host_ip, book_id,
                                                        current_user.id)
    requests.post(URI, data=jsonPUT, auth=HTTPBasicAuth(current_user.token,
                                                        null))
    return '/C'


@app.route("/User/login", methods=['POST'])
def userLogin():
    uname = request.form.get('uname')
    psw = request.form.get('psw')
    if addUserToLocalDB(uname, psw):
        user = User.query.filter_by(username=uname).first()
        login_user(user, remember=True)
    return redirect(url_for('index'))


@app.route("/User/logout")
@login_required
def userLogout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/User/loggedin", methods=['GET'])
def logged_in():
    user = current_user
    if user.is_authenticated:
        tokenExpiration = user.tokenLeaseStart + timedelta(seconds=550)
        return str(datetime.now() < tokenExpiration)
    else:
        return str(False)


@app.route("/User/register", methods=['GET', 'POST'])
def userRegister():
    form = request.form
    newUserData = form.to_dict(flat=False)
    register_new_user(**newUserData)

    return redirect('/')
