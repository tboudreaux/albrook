from .models import Author, Narrator, Genre, Tag, Series, Book, Track

class exists:
    @staticmethod
    def is_book(title):
        r = Book.query.filter_by(title=title).all()
        if len(r) == 0:
            return False
        else:
            return True

    @staticmethod
    def is_author(firstName, lastName):
        r = Author.query.filter_by(firstName=firstName, lastName=lastName).all()
        if len(r) == 0:
            return False
        else:
            return True

    @staticmethod
    def is_narrator(firstName, lastName):
        r = Narrator.query.filter_by(firstName=firstName, lastName=lastName).all()
        if len(r) == 0:
            return False
        else:
            return True

    @staticmethod
    def is_genre(genre):
        r = Genre.query.filter_by(name=genre).all()
        if len(r) == 0:
            return False
        else:
            return True

    @staticmethod
    def is_series(series):
        r = Series.query.filter_by(name=series).all()
        if len(r) == 0:
            return False
        else:
            return True

    @staticmethod
    def is_tag(tag):
        r = Tag.query.filter_by(name=tag).all()
        if len(r) == 0:
            return False
        else:
            return True
