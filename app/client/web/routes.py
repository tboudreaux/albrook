from web import app, host_ip
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from web.models import User
import requests
import json
from requests.auth import HTTPBasicAuth
from .auth import addUserToLocalDB

null = 'null'

# TODO -> get the modal to disaper when logged in
# TODO -> Get authenticated audio working
@app.route('/')
def index():
    URI = 'http://{}:5002/Books'.format(host_ip)
    if current_user.is_authenticated:
        response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
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
        info = {}
        forceLogin = True

    return render_template('index.html', **locals())


@app.route('/Book/id:<book_id>/chapter:<chapter_id>/stream')
def TrackStream(book_id, chapter_id):
    return 'http://{}:5002/Book/{}/{}/stream'.format(host_ip, book_id,
                                                     chapter_id)


@app.route('/Book/id:<book_id>/uid:<user_id>/currentTrack')
@login_required
def CurrentUserTrack(book_id, user_id):
    URI = 'http://{}:5002/Book/{}/user/{}/track'.format(host_ip, book_id,
                                                        user_id)
    response = requests.get(URI, auth=HTTPBasicAuth(current_user.token, null))
    return response.text


@app.route('/Author/name:<author_name>')
@login_required
def getAuthorInfo(author_name):
    URI = 'http://{}:5002/Author/name/{}'.format(host_ip, author_name)
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


@app.route('/Book/id:<book_id>/uid:<user_id>/currentTrack', methods=['POST'])
@login_required
def updateUserBookInfo(book_id, user_id):
    jsonPUT = request.get_json()
    URI = 'http://{}:5002/Book/{}/user/{}/track'.format(host_ip, book_id,
                                                        user_id)
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


@app.route("/User/logout", methods=['GET'])
@login_required
def userLogout():
    logout_user()
    return redirect(url_for('index'))
