from flask import Flask, Response, send_from_directory, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine, func
from flask_jsonpify import jsonify
from PIL import Image
import json
import os
from app.advQueryController import trackServer, userBookServer
from flask_login import current_user, login_user, login_required
from app import db
from app import auth
import names

from app import app
from app.utils import conditional_auth

api = Api(app)

import app.models as m

nullReturn = {'data': []}
unAuth  = Response('<Why access is denied string goes here...>', 401,
                  {'WWW-Authenticate':'Basic realm="Login Required"'})


def load_user(username):
    return m.User.query.filter_by(username=username).first()


@auth.verify_password
def verify_password(username_or_token, password):
    user = m.User.verify_auth_token(username_or_token)
    if not user:
        if not (username_or_token and password):
            return False
        else:
            user = m.User.query.filter_by(username = username_or_token).first()
            if not user:
                return False
            else:
                return user.check_password(password)
    return True


class Authors(Resource):
    @auth.login_required
    def get(self):
        r = m.Author.query.all()
        result = {'data': [x.to_dict() for x in r]}
        return jsonify(result)


class Author(Resource):
    @auth.login_required
    def get(self, author_id):
        r = m.Author.query.filter_by(id=author_id).all()
        result = {'data': [x.to_dict() for x in r]}
        return jsonify(result)


class AuthorByName(Resource):
    @auth.login_required
    def get(self, author_name):
        author_name = author_name.split(' ')
        r = m.Author.query.filter_by(firstName=author_name[0],
                                     lastName=author_name[-1])
        result = {'data': [x.to_dict() for x in r]}
        return jsonify(result)


class Books(Resource):
    @auth.login_required
    def get(self):
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


class Book(Resource):
    @auth.login_required
    def get(self, book_id):
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

class Thumbnail(Resource):
    def get(self, book_id, width, height):
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

class Cover(Resource):
    def get(self, book_id):
        imgPath = m.Book.query.filter_by(id=book_id).first().cover
        return send_from_directory('/'.join(imgPath.split('/')[:-1]),
                                   'cover.jpg')


class BookByTitle(Resource):
    @auth.login_required
    def get(self, book_title):
        r = m.Book.query.filter_by(title=book_title)
        result = {'data': [x.to_dict() for x in r]}
        return jsonify(result)


class BookTracks(Resource):
    @auth.login_required
    def get(self, book_id):
        r = m.Book.query.filter_by(id=book_id).first()
        if r:
            result = {'data': [x.to_dict() for x in r.tracks]}
        else:
            result = nullReturn
        return jsonify(result)

class otherBooksByAuthor(Resource):
    @auth.login_required
    def get(self, book_id):
        authors = m.Book.query.filter_by(id=book_id).first().authors
        books = list()
        for author in authors:
            books.extend(author.books)
        result = {'data': [x.to_dict() for x in books]}
        return jsonify(result)


class AuthorBooks(Resource):
    @auth.login_required
    def get(self, author_id):
        r = m.Author.query.filter_by(id=author_id).first()
        if r:
            result = {'data': [x.to_dict() for x in r.books]}
        else:
            result = nullReturn
        return jsonify(result)

class AuthorOfBook(Resource):
    @auth.login_required
    def get(self, book_id):
        r = m.Book.query.filter_by(id=book_id).first()
        if r:
            result = {'data': [x.to_dict() for x in r.authors]}
        else:
            result = nullReturn
        return jsonify(result)

class AuthorOfBookByTitle(Resource):
    @auth.login_required
    def get(self, book_title):
        r = m.Book.query.filter_by(title=book_title).all()
        if r:
            result = {'data': [x.to_dict() for x in r.authors]}
        else:
            result = nullReturn
        return jsonify(result)

class AuthorTumbnail(Resource):
    def get(self, author_id, width, height):
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

class Narrators(Resource):
    @auth.login_required
    def get(self):
        r = m.Narrator.query.all()
        result = {'data': [x.to_dict() for x in r]}
        return jsonify(result)

class Narrator(Resource):
    @auth.login_required
    def get(self, narrator_id):
        r = m.Narrator.query.filter_by(id=narrator_id).all()
        result = {'data': [x.to_dict() for x in r]}
        return jsonify(result)

class NarratorBooks(Resource):
    @auth.login_required
    def get(self, narrator_id):
        r = m.Narrator.query.filter_by(id=narrator_id).first()
        if r:
            result = {'data': [x.to_dict() for x in r.books]}
        else:
            result = nullReturn
        return jsonify(result)

class NarratorOfBookTitle(Resource):
    @auth.login_required
    def get(self, book_title):
        r = m.Book.query.filter_by(title=book_title).first()
        if r:
            result = {'data': [x.to_dict() for x in r.narrators]}
        else:
            result = nullReturn
        return jsonify(result)

class NarratorOfBook(Resource):
    @auth.login_required
    def get(self, book_id):
        r = m.Book.query.filter_by(id=book_id).first()
        if r:
            result = {'data': [x.to_dict() for x in r.narrators]}
        else:
            result = nullReturn
        return jsonify(result)

class TotalBooks(Resource):
    @auth.login_required
    def get(self):
        result = {'data': [{'Count': len(m.Book.query.all())}]}
        return jsonify(result)

class TotalBooksByAuthor(Resource):
    @auth.login_required
    def get(self, author_id):
        r = m.Author.query.filter_by(id=author_id).first()
        if r:
            number = len(r.books)
            result = {'data': [{'Count': number}]}
        else:
            result = nullReturn
        return jsonify(result)

class TrackInfo(Resource):
    @auth.login_required
    def get(self, book_id, chapter_id):
        track = trackServer.getChapter(book_id, chapter_id)
        return jsonify(track)

class TrackStream(Resource):
    def get(self, book_id, chapter_id):
        track = trackServer.getChapter(book_id, chapter_id)
        path = track['data'][0]['filePath']
        return send_from_directory('/'.join(path.split('/')[:-1]),
                                   path.split('/')[-1])

class CurrentTrack(Resource):
    @auth.login_required
    def get(self, book_id, user_id):
        track = userBookServer.getPickUpInformation(book_id, user_id)
        return jsonify(track)

    @auth.login_required
    def post(self, book_id, user_id):
        record = userBookServer.updateTrackInfo(user_id, book_id,
                                       request.form['currentChapter'],
                                       request.form['currentLocation'])
        if record:
            db.session.add(record)
        db.session.commit()

class GenerateToken(Resource):
    @auth.login_required
    def get(self, username):
        print(username)
        user = m.User.query.filter_by(username=username).first()
        token = user.generate_auth_token()
        return jsonify({ 'token': token.decode('ascii') })

class UserInfo(Resource):
    @auth.login_required
    def get(self, username):
        user = m.User.query.filter_by(username=username).first()
        return jsonify(user.to_dict())

class UserExists(Resource):
    def get(self, username):
        exists = m.User.query.filter_by(username=username).first()
        return jsonify({"data": [{"exists": exists==True}]})

# TODO -> Get conditional decorator to Work
#         so that auth is requred always
#         except when 0 users are registered
class RegisterUser(Resource):
    # @conditional_auth
    def post(self):
        newUser = m.User()
        newUser.username = request.form['username']
        newUser.firstName = request.form['firstname']
        newUser.middleName = request.form['middlename']
        newUser.lastName = request.form['lastname']
        newUser.email = request.form['email']
        newUser.set_password(request.form['password'])

        newDevice = m.Device()
        newDevice.deviceName = names.get_last_name()
        newDevice.lastIP = request.remote_addr
        newDevice.lastConnect = 'now'
        newDevice.deviceType = request.form['platform']

        db.session.add(newDevice)
        dses= m.Device.query.filter_by(deviceName=newDevice.deviceName).first()

        newUser.lastDeviceID = dses.id

        db.session.add(newUser)
        db.session.commit()
        return jsonify({'data': [{"registered": newUser.username}]})

class UserNumber(Resource):
    def get(self):
        users = len(m.User.query.all())
        return jsonify({'data': [{'number': users}]})


api.add_resource(Authors, '/Authors')                         # Get all Authors
api.add_resource(Author, '/Author/<author_id>')               # Get a given Author By ID
api.add_resource(AuthorBooks, '/Author/<author_id>/books')    # Get all books of an author
api.add_resource(AuthorOfBook, '/Author/book_id/<book_id>')
api.add_resource(AuthorOfBookByTitle, '/Author/title/<book_title>')
api.add_resource(AuthorByName, '/Author/name/<author_name>')
api.add_resource(AuthorTumbnail, '/Author/<author_id>/portrait/thumbnail:<width>:<height>')
api.add_resource(otherBooksByAuthor, '/Books/author/<book_id>')

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
api.add_resource(GenerateToken, '/User/<username>/token')
api.add_resource(UserInfo, '/User/<username>/info')
api.add_resource(UserExists, '/User/<username>/exists')
api.add_resource(RegisterUser, '/User/register/')
api.add_resource(UserNumber, '/User/number')


if __name__ == '__main__':
    app.run(port='5002')
