from app import db
from app import app
from flask_login import UserMixin
from .association import associationTables
from .serializableBase import SerializableModel
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class Track(SerializableModel):
    __tablename__ = 'track'
    id = db.Column(db.Integer, primary_key=True)
    filePath = db.Column(db.String(1024), nullable=False, unique=True)
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    chapter = db.Column(db.Integer)

    _default_fields = [
        'filePath',
        'bookID',
        'chapter'
    ]

    def __repr__(self):
        return "<Track {} Book {}>".format(self.id, self.bookID)

class Book(SerializableModel):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True, unique=True, index=True)
    publicationDate = db.Column(db.String(10))
    description = db.Column(db.Text)
    chapters = db.Column(db.Integer, nullable=False)
    cover = db.Column(db.String(1024))
    hasFilm = db.Column(db.Boolean)

    tracks = db.relationship(Track, lazy="joined",
                             backref=db.backref('book', lazy='joined'))

    _default_fields = [
        'title',
        'publicationDate',
        'description',
        'chapters',
        'cover',
        'hasFilm'
    ]

    def __repr__(self):
        return "<Book {}>".format(self.title)

class Author(SerializableModel):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(128), index=True, nullable=False)
    middleName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    biography = db.Column(db.Text)
    profileImage = db.Column(db.String(1024))
    nationality = db.Column(db.String(128))

    books = db.relationship(Book, secondary=associationTables.AuthorBook,
                           lazy='subquery',
                           backref=db.backref('authors', lazy=True))

    _default_fields = [
        'firstName',
        'middleName',
        'lastName',
        'biography',
        'profileImage',
        'nationality'
    ]

    def __repr__(self):
        return '<Author {} {}>'.format(self.firstName, self.lastName)

class Narrator(SerializableModel):
    __tablename__ = 'narrator'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(128), index=True, nullable=False)
    middleName = db.Column(db.String(128))
    lastName = db.Column(db.String(128))
    biography = db.Column(db.Text)
    profileImage = db.Column(db.String(1024))
    nationality = db.Column(db.String(128))

    books = db.relationship(Book, secondary=associationTables.NarratorBook,
                           lazy='subquery',
                           backref=db.backref('narrators', lazy=True))

    _default_fields = [
        'firstName',
        'middleName',
        'lastName',
        'biography',
        'profileImage',
        'nationality'
    ]

    def __repr__(self):
        return '<Narrator {} {}>'.format(self.firstName, self.lastName)

class Genre(SerializableModel):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, index=True)
    description = db.Column(db.Text)

    book = db.relationship(Book, secondary=associationTables.GenreBook,
                           lazy='subquery',
                           backref=db.backref('genres', lazy=True))

    _default_fields = [
        'name',
        'description'
    ]

    def __repr__(self):
        return '<Genre {}>'.format(self.name)

class Device(SerializableModel):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    deviceName = db.Column(db.String(32), nullable=False)
    lastIP = db.Column(db.String(32), nullable=False)
    lastConnect = db.Column(db.String(19), nullable=False)
    deviceType = db.Column(db.String(32))

    _default_fields = [
        'deviceName',
        'deviceType',
        'lastIP',
        'lastConnect',
        'deviceType'
    ]

    def __repr__(self):
        return "<Device {}>".format(self.deviceName)

class Tag(SerializableModel):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)

    book = db.relationship(Book, secondary=associationTables.TagBook,
                           lazy='subquery',
                           backref=db.backref('tags', lazy=True))

    _default_fields = [
        'name'
    ]

    def __repr__(self):
        return "<Tag {}>".format(self.name)

class Series(SerializableModel):
    __tablename__ = 'series'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)

    book = db.relationship(Book, secondary=associationTables.SeriesBook,
                           lazy='subquery',
                           backref=db.backref('series', lazy=True))

    _default_fields = [
        'name',
        'description'
    ]

    def __repr__(self):
        return "<Series {}>".format(self.name)

class UserBook(SerializableModel):
    __tablename__ = 'user_book'
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'),
                       primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'),
                       primary_key=True)
    lastOpened = db.Column(db.DateTime, nullable=False)
    lastLocation = db.Column(db.Float, nullable=False)
    lastChapter = db.Column(db.Integer, nullable=False)
    book = db.relationship(Book, backref=db.backref("user_link", lazy='joined'))
    user = db.relationship('User', backref=db.backref("book_link", lazy='joined'))


    _default_fields = [
        "bookId",
        "userID",
        "lastOpened",
        "lastLocation",
        "lastChapter"
         ]

    def __repr__(self):
        return "<book {} user {}>".format(self.bookID, self.userID)

class User(SerializableModel):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(128), index=True, nullable=False)
    middleName = db.Column(db.String(128))
    lastName = db.Column(db.String(128), index=True)
    biography = db.Column(db.Text)
    profileImage = db.Column(db.String(1024))
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    passwordHash = db.Column(db.String(1024))
    lastDeviceID = db.Column(db.Integer, db.ForeignKey('device.id'),
                           nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(128), unique=True)

    books = db.relationship(Book, secondary="user_book",
                           lazy='subquery',
                           backref=db.backref('books', lazy=True))
    device = db.relationship(Device, backref='lastUser', lazy=True,
                             uselist=False)

    _default_fields = [
         'firstName',
         'middleName',
         'lastName',
         'biography',
         'profileImage',
         'username',
         'email',
         'lastDeviceID'
         ]

    _hidden_fields = [
        "passwordHash",
    ]

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.passwordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.passwordHash, password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
