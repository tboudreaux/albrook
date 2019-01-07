from flask import Flask
from flask import render_template
import socket
import requests
import json

app = Flask(__name__)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)


@app.route('/')
@app.route('/index')
def books():
    response = requests.get('http://{}:5002/Books'.format(host_ip))
    json_data = json.loads(response.text)
    books = json_data['data']
    numBooks = len(books)
    titles = [x['Title'] for x in books]
    descs = [x['Description'].replace('\\n', '<br>') for x in books]
    authors = [x['Authors'] for x in books]
    narrators = [x['Narrators'] for x in books]

    info = {"titles": titles, "descs": descs, 'authors': authors, 'narrators': narrators}

    return render_template('index.html', **locals())


@app.route('/Book/id:<book_id>/chapter:<chapter_id>/stream')
def TrackStream(book_id, chapter_id):
    return 'http://{}:5002/Book/{}/{}/stream'.format(host_ip, book_id, chapter_id)


@app.route('/Book/id:<book_id>/uid:<user_id>/currentTrack')
def CurrentUserTrack(book_id, user_id):
    response = requests.get('http://{}:5002/Book/{}/user/{}/track'.format(host_ip, book_id, user_id))
    return response.text


@app.route('/Author/name:<author_name>')
def getAuthorInfo(author_name):
    response = requests.get('http://{}:5002/Author/name/{}'.format(host_ip, author_name))
    return response.text


@app.route('/Book/id:<book_id>/cover/width:<width>/height:<height>')
def getCoverURI(book_id, width, height):
    return 'http://{}:5002/Book/{}/cover/thumbnail:{}:{}'.format(host_ip, book_id, width, height)


@app.route('/Author/id:<author_id>/portrait/width:<width>/height:<height>')
def getAuthorPortaitURI(author_id, width, height):
    return 'http://{}:5002/Author/{}/portrait/thumbnail:{}:{}'.format(host_ip, author_id, width, height)