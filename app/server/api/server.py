from flask import Flask, Response, send_from_directory, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from flask_jsonpify import jsonify
from PIL import Image
import json
import os
import trackServer
import userBookServer

db_connect = create_engine('sqlite:///../../db/albrook.db')
app = Flask(__name__)
api = Api(app)


class Authors(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Authors")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Author(Resource):
    def get(self, author_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Authors WHERE UID = {}".format(author_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class AuthorByName(Resource):
    def get(self, author_name):
        if author_name.count(' ') == 1:
            author_name = author_name.replace(' ', '  ')
        conn = db_connect.connect()
        query = conn.execute("""SELECT * FROM Authors WHERE
                             printf('%s %s %s', Authors.FirstName,
                             Authors.MiddleName, Authors.LastName)
                             == \"{}\"""".format(author_name))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Books(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Books")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        for book in result['data']:
            uid = book['UID']
            query = conn.execute("""SELECT printf('%s %s %s', Authors.FirstName, Authors.MiddleName, Authors.LastName) 
                                    AS NAME FROM Books INNER JOIN AuthorsBooks
                                    ON Books.UID = AuthorsBooks.BookID INNER JOIN Authors
                                    ON Authors.UID = AuthorsBooks.AuthorID WHERE 
                                    Books.UID = {} GROUP BY Authors.FirstName """.format(uid))
            authorsInfos = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            authorList = list()
            for author in authorsInfos['data']:
                authorList.append(author['NAME'].replace('  ', ' '))
            book['Authors'] = authorList

            query = conn.execute("""SELECT printf('%s %s %s', Narrators.FirstName, Narrators.MiddleName, Narrators.LastName) 
                                    AS NAME FROM Books INNER JOIN NarratorsBooks
                                    ON Books.UID = NarratorsBooks.BookID INNER JOIN Narrators
                                    ON Narrators.UID = NarratorsBooks.NarratorID WHERE 
                                    Books.UID = {} GROUP BY Narrators.FirstName """.format(uid))
            NarratorsInfos = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            narratorList = list()
            for narrator in NarratorsInfos['data']:
                narratorList.append(narrator['NAME'].replace('  ', ' '))
            book['Narrators'] = narratorList
        return jsonify(result)


class Book(Resource):
    def get(self, book_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Books WHERE UID = {}".format(book_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        for book in result['data']:
            uid = book['UID']
            query = conn.execute("""SELECT printf('%s %s %s', Authors.FirstName, Authors.MiddleName, Authors.LastName) 
                                    AS NAME FROM Books INNER JOIN AuthorsBooks
                                    ON Books.UID = AuthorsBooks.BookID INNER JOIN Authors
                                    ON Authors.UID = AuthorsBooks.AuthorID WHERE 
                                    Books.UID = {} GROUP BY Authors.FirstName """.format(uid))
            authorsInfos = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            authorList = list()
            for author in authorsInfos['data']:
                authorList.append(author['NAME'].replace('  ', ' '))
            book['Authors'] = authorList

            query = conn.execute("""SELECT printf('%s %s %s', Narrators.FirstName, Narrators.MiddleName, Narrators.LastName) 
                                    AS NAME FROM Books INNER JOIN NarratorsBooks
                                    ON Books.UID = NarratorsBooks.BookID INNER JOIN Narrators
                                    ON Narrators.UID = NarratorsBooks.NarratorID WHERE 
                                    Books.UID = {} GROUP BY Narrators.FirstName """.format(uid))
            NarratorsInfos = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
            narratorList = list()
            for narrator in NarratorsInfos['data']:
                narratorList.append(narrator['NAME'].replace('  ', ' '))
            book['Narrators'] = narratorList
        return jsonify(result)

class Thumbnail(Resource):
    def get(self, book_id, width, height):
        conn = db_connect.connect()
        query = conn.execute("SELECT Cover FROM Books WHERE UID = {}".format(book_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        imgPath = result['data'][0]['Cover']
        filename = '{}_thumbnail:{}:{}.{}'.format('.'.join(imgPath.split('.')[:-1]), width, height, imgPath.split('.')[-1])
        if not os.path.exists(filename):
            im = Image.open(imgPath)
            im.thumbnail((int(width), int(height)))
            im.save(filename, "JPEG")

        return send_from_directory('/'.join(imgPath.split('/')[:-1]), 'cover_thumbnail:{}:{}.jpg'.format(width, height))

class Cover(Resource):
    def get(self, book_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT Cover FROM Books WHERE UID = {}".format(book_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        imgPath = result['data'][0]['Cover']
        return send_from_directory('/'.join(imgPath.split('/')[:-1]), 'cover.jpg')


class BookByTitle(Resource):
    def get(self, book_title):
        print(book_title)
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Books WHERE Title = \"{}\"".format(book_title))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class BookTracks(Resource):
    def get(self, book_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Tracks WHERE BookID = {}".format(book_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class AuthorBooks(Resource):
    def get(self, author_id):
        conn = db_connect.connect()
        query = conn.execute("""SELECT Books.* FROM Books INNER JOIN AuthorsBooks 
                                ON Books.UID = AuthorsBooks.BookID INNER JOIN
                                Authors ON Authors.UID = AuthorsBooks.AuthorID
                                WHERE Authors.UID = {}""".format(author_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class AuthorOfBook(Resource):
    def get(self, book_id):
        conn = db_connect.connect()
        query = conn.execute("""SELECT Authors.* FROM Books INNER JOIN AuthorsBooks
                                ON Books.UID = AuthorsBooks.BookID INNER JOIN Authors
                                ON Authors.UID = AuthorsBooks.AuthorID WHERE 
                                Books.UID = {} GROUP BY Authors.FirstName """.format(book_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class AuthorOfBookByTitle(Resource):
    def get(self, book_title):
        conn = db_connect.connect()
        query = conn.execute("""SELECT Authors.* FROM Books INNER JOIN AuthorsBooks
                                ON Books.UID = AuthorsBooks.BookID INNER JOIN Authors
                                ON Authors.UID = AuthorsBooks.AuthorID WHERE 
                                UPPER(Books.Title) = UPPER(\"{}\") GROUP BY 
                                Authors.FirstName """.format(book_title))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class AuthorTumbnail(Resource):
    def get(self, author_id, width, height):
        conn = db_connect.connect()
        query = conn.execute("SELECT ProfileImage FROM Authors WHERE UID = {}".format(author_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        imgPath = result['data'][0]['ProfileImage']
        filename = '{}_thumbnail:{}:{}.{}'.format('.'.join(imgPath.split('.')[:-1]), width, height, imgPath.split('.')[-1])
        if not os.path.exists(filename):
            im = Image.open(imgPath)
            im.thumbnail((int(width), int(height)))
            im.save(filename, "JPEG")

        return send_from_directory('/'.join(imgPath.split('/')[:-1]), 'portrait_thumbnail:{}:{}.jpg'.format(width, height))


class Narrators(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Narrators")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Narrator(Resource):
    def get(self, narrator_id):
        conn = db_connect.connect()
        query = conn.execute("SELECT * FROM Narrators WHERE UID = {}".format(narrator_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class NarratorBooks(Resource):
    def get(self, narrator_id):
        conn = db_connect.connect()
        query = conn.execute("""SELECT Books.* FROM Books INNER JOIN NarratorsBooks 
                                ON Books.UID = NarratorsBooks.BookID INNER JOIN
                                Narrators ON Narrators.UID = NarratorsBooks.NarratorID
                                WHERE Narrators.UID = {}""".format(narrator_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class NarratorOfBook(Resource):
    def get(self, book_title):
        conn = db_connect.connect()
        query = conn.execute("""SELECT Narrators.* FROM Narrators INNER JOIN NarratorsBooks
                                ON Narrators.UID = NarratorsBooks.NarratorID INNER JOIN
                                Books ON NarratorsBooks.BookID = Books.UID WHERE
                                UPPER(Books.Title) = UPPER(\"{}\") GROUP BY 
                                Narrators.FirstName""".format(book_title))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class TotalBooks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("""SELECT COUNT(UID) AS BOOKS FROM Books""")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class TotalBooksByAuthor(Resource):
    def get(self, author_id):
        conn = db_connect.connect()
        query = conn.execute("""SELECT COUNT(Books.UID) AS BOOKS FROM Books JOIN AuthorsBooks
                                ON Books.UID = AuthorsBooks.BookID JOIN Authors ON
                                AuthorsBooks.AuthorID = Authors.UID WHERE
                                Authors.UID = \"{}\"""".format(author_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class TrackInfo(Resource):
    def get(self, book_id, chapter_id):
        track = trackServer.getChapter(db_connect, book_id, chapter_id)
        return jsonify(track)

class TrackStream(Resource):
    def get(self, book_id, chapter_id):
        track = trackServer.getChapter(db_connect, book_id, chapter_id)
        path = track['data'][0]['FilePath']
        return send_from_directory('/'.join(path.split('/')[:-1]), path.split('/')[-1])

class CurrentTrack(Resource):
    def get(self, user_id, book_id):
        track = userBookServer.getPickUpInformation(db_connect, book_id, user_id)
        return jsonify(track)

    def put(self, user_id, book_id):
        userBookServer.updateTrackInfo(db_connect, user_id, book_id,
                                       request.form['currentChapter'],
                                       request.form['currentLocation'])


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
api.add_resource(NarratorOfBook, '/Narrators/title/<book_title>')

api.add_resource(TotalBooks, '/TotalBooks')
api.add_resource(TotalBooksByAuthor, '/TotalBooks/<author_id>')

api.add_resource(TrackInfo, '/Book/<book_id>/<chapter_id>/info')
api.add_resource(TrackStream, '/Book/<book_id>/<chapter_id>/stream')
api.add_resource(CurrentTrack, '/Book/<book_id>/user/<user_id>/track')


if __name__ == '__main__':
    app.run(port='5002')
