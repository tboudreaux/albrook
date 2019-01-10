from app import db

class associationTables:
    AuthorBook = db.Table('AuthorBook',
        db.Column('bookID', db.Integer, db.ForeignKey('book.id')),
        db.Column('authorID', db.Integer, db.ForeignKey('author.id'))
    )

    NarratorBook = db.Table('NarratorBook',
        db.Column('bookID', db.Integer, db.ForeignKey('book.id')),
        db.Column('narratorID', db.Integer, db.ForeignKey('narrator.id'))
    )

    GenreBook = db.Table('GenreBook',
        db.Column('bookID', db.Integer, db.ForeignKey('book.id')),
        db.Column('genreID', db.Integer, db.ForeignKey('genre.id'))
    )

    TagBook = db.Table('TagBook',
        db.Column('bookID', db.Integer, db.ForeignKey('book.id')),
        db.Column('tagID', db.Integer, db.ForeignKey('tag.id'))
    )

    SeriesBook = db.Table('SeriesBook',
        db.Column('bookID', db.Integer, db.ForeignKey('book.id')),
        db.Column('seriesID', db.Integer, db.ForeignKey('series.id'))
    )
