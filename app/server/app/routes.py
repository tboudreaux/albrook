from flask import Flask, Response, send_from_directory, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, func
from flask_jsonpify import jsonify
from PIL import Image
import json
import os
from .advQueryController import trackServer, userBookServer
from flask_login import current_user, login_user

from app import app

db_connect = create_engine('sqlite:///../../db/albrook.db')
api = Api(app)

import app.models as m

nullReturn = {'data': []}
unAuth  = Response('<Why access is denied string goes here...>', 401,
                  {'WWW-Authenticate':'Basic realm="Login Required"'})

class Authors(Resource):
    def get(self):
        if current_user.is_authenticated:
            r = m.Author.query.all()
            result = {'data': [x.to_dict() for x in r]}
            return jsonify(result)
        else:
            return unAuth


class Author(Resource):
    def get(self, author_id):
        if current_user.is_authenticated:
            r = m.Author.query.filter_by(id=author_id).all()
            result = {'data': [x.to_dict() for x in r]}
            return jsonify(result)
        else:
            return unAuth


class AuthorByName(Resource):
    def get(self, author_name):
        if current_user.is_authenticated:
            author_name = author_name.split(' ')
            r = m.Author.query.filter_by(firstName=author_name[0],
                                         lastName=author_name[-1])
            result = {'data': [x.to_dict() for x in r]}
            return jsonify(result)
        else:
            return unAuth


class Books(Resource):
    def get(self):
        if current_user.is_authenticated:
            r = m.Book.query.all()
            result = {'data': [x.to_dict() for x in r]}
            for book, bookDict in zip(r, result['data']):
                authors = book.authors
                authorsInfos = {'data': [x.to_dict() for x in authors]}
                authorList = list()
                for author in authorsInfos['data']:
                    name = [author['firstName'], author['lastName']]
                    if author['middleName']:
                        name.insert(1, author['middleName'])
                    authorList.append(' '.join(name))
                print('AuthorList: ', authorList)
                bookDict['Authors'] = authorList

                narrators = book.narrators
                narratorsInfos = {'data': [x.to_dict() for x in narrators]}
                narratorList = list()
                for narrator in narratorsInfos['data']:
                    name = [narrator['firstName'], narrator['lastName']]
                    if narrator['middleName']:
                        name.insert(1, narrator['middleName'])
                    narratorList.append(' '.join(name))
                bookDict['Narrators'] = narratorList
            return jsonify(result)
        else:
            return unAuth


class Book(Resource):
    def get(self, book_id):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(id=book_id).all()
            result = {'data': [x.to_dict() for x in r]}
            for book, bookDict in zip(r, result['data']):
                authors = book.authors
                authorsInfos = {'data': [x.to_dict() for x in authors]}
                authorList = list()
                for author in authorsInfos['data']:
                    name = [author['firstName'], author['lastName']]
                    if author['middleName']:
                        name.insert(1, author['middleName'])
                    authorList.append(' '.join(name))

                bookDict['Authors'] = authorList

                narrators = book.narrators
                narratorsInfos = {'data': [x.to_dict() for x in narrators]}
                narratorList = list()
                for narrator in narratorsInfos['data']:
                    name = [narrator['firstName'], narrator['lastName']]
                    if narrator['middleName']:
                        name.insert(1, narrator['middleName'])
                    narratorList.append(' '.join(name))
                bookDict['Narrators'] = narratorList
            return jsonify(result)
        else:
            return unAuth

class Thumbnail(Resource):
    def get(self, book_id, width, height):
        if current_user.is_authenticated:
            imgPath = m.Book.query.filter_by(id=book_id).first().cover
            filename = '{}_thumbnail:{}:{}.{}'.format('.'.join(imgPath.split('.')[:-1]),
                                                      width, height,
                                                      imgPath.split('.')[-1])
            if not os.path.exists(filename):
                im = Image.open(imgPath)
                im.thumbnail((int(width), int(height)))
                im.save(filename, "JPEG")

            return send_from_directory('/'.join(imgPath.split('/')[:-1]),
                                       'cover_thumbnail:{}:{}.jpg'.format(width,
                                                                          height))
        else:
            return unAuth

class Cover(Resource):
    def get(self, book_id):
        if current_user.is_authenticated:
            imgPath = m.Book.query.filter_by(id=book_id).first().cover
            return send_from_directory('/'.join(imgPath.split('/')[:-1]),
                                       'cover.jpg')
        else:
            return unAuth


class BookByTitle(Resource):
    def get(self, book_title):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(title=book_title)
            result = {'data': [x.to_dict() for x in r]}
            return jsonify(result)
        else:
            return unAuth


class BookTracks(Resource):
    def get(self, book_id):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(id=book_id).first()
            if r:
                result = {'data': [x.to_dict() for x in r.tracks]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth


class AuthorBooks(Resource):
    def get(self, author_id):
        if current_user.is_authenticated:
            r = m.Author.query.filter_by(id=author_id).first()
            if r:
                result = {'data': [x.to_dict() for x in r.books]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class AuthorOfBook(Resource):
    def get(self, book_id):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(id=book_id).first()
            if r:
                result = {'data': [x.to_dict() for x in r.authors]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class AuthorOfBookByTitle(Resource):
    def get(self, book_title):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(title=book_title).all()
            if r:
                result = {'data': [x.to_dict() for x in r.authors]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class AuthorTumbnail(Resource):
    def get(self, author_id, width, height):
        if current_user.is_authenticated:
            imgPath = m.Author.query.filter_by(id=author_id).first().profileImage
            filename = '{}_thumbnail:{}:{}.{}'.format('.'.join(imgPath.split('.')[:-1]),
                                                      width, height,
                                                      imgPath.split('.')[-1])
            if not os.path.exists(filename):
                im = Image.open(imgPath)
                im.thumbnail((int(width), int(height)))
                im.save(filename, "JPEG")

            return send_from_directory('/'.join(imgPath.split('/')[:-1]),
                                       'portrait_thumbnail:{}:{}.jpg'.format(width,
                                                                            height))
        else:
            return unAuth


class Narrators(Resource):
    def get(self):
        if current_user.is_authenticated:
            r = m.Narrator.query.all()
            result = {'data': [x.to_dict() for x in r]}
            return jsonify(result)
        else:
            return unAuth

class Narrator(Resource):
    def get(self, narrator_id):
        if current_user.is_authenticated:
            r = m.Narrator.query.filter_by(id=narrator_id).all()
            result = {'data': [x.to_dict() for x in r]}
            return jsonify(result)
        else:
            return unAuth


class NarratorBooks(Resource):
    def get(self, narrator_id):
        if current_user.is_authenticated:
            r = m.Narrator.query.filter_by(id=narrator_id).first()
            if r:
                result = {'data': [x.to_dict() for x in r.books]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class NarratorOfBookTitle(Resource):
    def get(self, book_title):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(title=book_title).first()
            if r:
                result = {'data': [x.to_dict() for x in r.narrators]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class NarratorOfBook(Resource):
    def get(self, book_id):
        if current_user.is_authenticated:
            r = m.Book.query.filter_by(id=book_id).first()
            if r:
                result = {'data': [x.to_dict() for x in r.narrators]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class TotalBooks(Resource):
    def get(self):
        if current_user.is_authenticated:
            result = {'data': [{'Count': len(m.Book.query.all())}]}
            return jsonify(result)
        else:
            return unAuth

class TotalBooksByAuthor(Resource):
    def get(self, author_id):
        if current_user.is_authenticated:
            r = m.Author.query.filter_by(id=author_id).first()
            if r:
                number = len(r.books)
                result = {'data': [{'Count': number}]}
            else:
                result = nullReturn
            return jsonify(result)
        else:
            return unAuth

class TrackInfo(Resource):
    def get(self, book_id, chapter_id):
        if current_user.is_authenticated:
            track = trackServer.getChapter(book_id, chapter_id)
            return jsonify(track)
        else:
            return unAuth

class TrackStream(Resource):
    def get(self, book_id, chapter_id):
        if current_user.is_authenticated:
            track = trackServer.getChapter(book_id, chapter_id)
            path = track['data'][0]['filePath']
            return send_from_directory('/'.join(path.split('/')[:-1]),
                                       path.split('/')[-1])
        else:
            return unAuth

class CurrentTrack(Resource):
    def get(self, book_id, user_id):
        if current_user.is_authenticated:
            track = userBookServer.getPickUpInformation(db_connect, book_id, user_id)
            return jsonify(track)
        else:
            return unAuth

    def post(self, book_id, user_id):
        if current_user.is_authenticated:
            userBookServer.updateTrackInfo(user_id, book_id,
                                           request.form['currentChapter'],
                                           request.form['currentLocation'])
        else:
            return unAuth

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'user': current_user.username})
    user = User.query.filter_by(request.username=username).first()
    if user is None or not user.check_password(request.password):
        return jsonify({'user': None})
    login_user(user, remember=request.remember_me)
    return {'user': current_user.username}


api.add_resource(Authors, '/Authors')                         # Get all Authors
api.add_resource(Author, '/Author/<author_id>')               # Get a given Author By ID
api.add_resource(AuthorBooks, '/Author/<author_id>/books')    # Get all books of an author
api.add_resource(AuthorOfBook, '/Author/book_id/<book_id>')
api.add_resource(AuthorOfBookByTitle, '/Author/title/<book_title>')
api.add_resource(AuthorByName, '/Author/name/<author_name>')
api.add_resource(AuthorTumbnail, '/Author/<author_id>/portrait/thumbnail:<width>:<height>')

api.add_resource(Books, '/Books')                             # Get All Books
api.add_resource(Book, '/Book/<book_id>')                     # Get a given book by ID
api.add_resource(Thumbnail, '/Book/<book_id>/cover/thumbnail:<width>:<height>')
api.add_resource(Cover, '/Book/<book_id>/cover')
api.add_resource(BookTracks, '/Book/<book_id>/tracks')        # All trakcs of a given book by id
api.add_resource(BookByTitle, '/Book/title/<book_title>')     # Get Book By Book Title

api.add_resource(Narrators, '/Narrators')
api.add_resource(Narrator, '/Narrator/<narrator_id>')
api.add_resource(NarratorBooks, '/Narrator/<narrator_id>/books')
api.add_resource(NarratorOfBookTitle, '/Narrator/book/title/<book_title>')
api.add_resource(NarratorOfBook, '/Narrator/book/id/<book_id>')

api.add_resource(TotalBooks, '/TotalBooks')
api.add_resource(TotalBooksByAuthor, '/TotalBooks/<author_id>')
#
api.add_resource(TrackInfo, '/Book/<book_id>/<chapter_id>/info')
api.add_resource(TrackStream, '/Book/<book_id>/<chapter_id>/stream')
api.add_resource(CurrentTrack, '/Book/<book_id>/user/<user_id>/track')


if __name__ == '__main__':
    app.run(port='5002')
