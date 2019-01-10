from app import db
from .models import Author, Narrator, Genre, Tag, Series, Book, Track
from .models import Device, User, UserBook
from .elementExistsInDB import exists
from .utils import file_is_of_type, get_file_type, sort_nicely
import os
import json
from datetime import datetime


IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'tiff']


def add_author(authorName, pathToAuthor):
    author = Author()
    FullName = authorName.split(' ')
    author.firstName = FullName[0]
    author.lastName = FullName[-1]
    if not exists.is_author(author.firstName, author.lastName):
        if len(FullName) > 2:
            author.middleName = FullName[1]
        files = os.listdir(pathToAuthor)
        if 'author.json' in files:
            with open(os.path.join(pathToAuthor, 'author.json')) as f:
                data = json.load(f)
            author.biography = data['Biography']
            author.nationality = data['Nationality']
        for file in files:
            if "portrait" == file.split('.')[0]:
                if get_file_type(os.path.join(pathToAuthor, file)).lower() in IMAGE_TYPES:
                    author.profileImage = '{}'.format(os.path.join(pathToAuthor, file))

        db.session.add(author)
        return author
    else:
        return Author.query.filter_by(firstName=FullName[0],
                                      lastName=FullName[-1]).first()


def add_tracks(pathToBook):
    chapters = os.listdir(pathToBook)
    chapters = [x for x in chapters if file_is_of_type(x, 'mp3')]
    tracks = list()
    for chapterNum, chapter in enumerate(sort_nicely(chapters)):
        T = Track(filePath=os.path.join(pathToBook, chapter),
                  chapter=chapterNum)
        tracks.append(T)
    return tracks


def add_genre(genre):
    if not exists.is_genre(genre):
        genre = Genre(name=genre)
        db.session.add(genre)
        return genre
    else:
        return Genre.query.filter_by(name=genre).first()


def add_narrator(name, narratorPath):
    narrator = Narrator()
    orig = name
    name = name.replace(' ', '')
    name = name.replace('.', '')
    narratorJSON = os.path.join(narratorPath, '{}.json'.format(name))

    if os.path.exists(narratorJSON):
        with open(narratorJSON) as f:
            data = json.load(f)

        narrator.biography = data['Biography']
        narrator.firstName = data['FirstName']
        narrator.lastName = data['LastName']
        narrator.middleName = data['MiddleName']
        narrator.profileImage = data['ProfileImage']
        narrator.nationality = data['Nationality']

    else:
        FullName = orig.split(' ')
        narrator.firstName = FullName[0]
        narrator.lastName = FullName[-1]

        if len(FullName) > 2:
            narrator.middleName = FullName[1]

    if not exists.is_narrator(narrator.firstName, narrator.lastName):
        db.session.add(narrator)
        return narrator
    else:
        return Narrator.query.filter_by(firstName = narrator.firstName,
                                        lastName = narrator.lastName).first()

def add_series(name, seriesPath):
    series = Series()
    seriseName = name.replace(' ', '')
    seriseJSON = os.path.join(seriesPath, '{}.json'.format(series))
    if os.path.exists(seriseJSON):
        with open(seriseJSON) as f:
            data = json.load(f)

        series.description = data['Description']
        series.name = data['Name']
    else:
        series.name = name
    if not exists.is_series(name):
        db.session.add(series)
        return series
    else:
        return Series.query.filter_by(name=name).first()


def add_tag(tag):
    if not exists.is_tag(tag):
        tag = Tag(name=tag)
        db.session.add(tag)
        return tag
    else:
        return Tag.query.filter_by(name=tag).first()


def add_book(pathToBook, files, narratorPath, seriesPath):
    rootSplit = pathToBook.split('/')
    backPath = '/'.join(rootSplit[:-1])
    Title = rootSplit[-1]
    if not exists.is_book(Title):
        commit = True
        book = Book()
        tracks = add_tracks(pathToBook)


        if "book.json" in files:
            with open(os.path.join(pathToBook, "book.json")) as f:
                data = json.load(f)

            fields = data.keys()
            if 'Title' in fields:
                Title = data['Title']

            if exists.is_book(Title):
                commit = False

            if commit:
                book.tracks = tracks
                book.chapters = len(tracks)
                book.title = Title

            if "Authors" in fields and commit:
                for author in data['Authors']:
                    book.authors.append(add_author(author, backPath))
            elif commit:
                book.authors.append(add_author(rootSplit[-2], backPath))

            if 'Description' in fields and commit:
                book.description = data['Description']

            if 'PublicationDate' in fields and commit:
                book.publicationDate = data['PublicationDate']

            if 'Narrators' in fields and commit:
                for narrator in data['Narrators']:
                    book.narrators.append(add_narrator(narrator, narratorPath))

            if "Genres" in fields and commit:
                for genre in data['Genres']:
                    book.genres.append(add_genre(genre))

            if "Series" in fields and commit:
                for series in data['Series']:
                    book.series.append(add_series(series, seriesPath))

            if "Tags" in fields and commit:
                for tag in data['Tags']:
                    book.tags.append(add_tag(tag))


        for file in files:
            if "cover" == file.split('.')[0]:
                coverPath = os.path.join(pathToBook, file)
                if get_file_type(coverPath).lower() in IMAGE_TYPES and commit:
                    book.cover = coverPath

        if commit:
            db.session.add(book)
            for track in tracks:
                db.session.add(track)
            db.session.commit()


def get_file_structure(Books, Narrators, Series):
    for i, (Books, dirs, files) in enumerate(os.walk(Books, topdown=False)):
        bookfound = False
        for file in files:
            if file_is_of_type(file, 'mp3'):
                bookfound = True
        if bookfound:
            add_book(Books, files, Narrators, Series)

def SampleDataScan():
    # os.remove('app/albrook.db')
    # db.create_all()
    Books = "/Users/tboudreaux/Programing/Albrook/SampleData/Audiobooks/"
    Narrators = "/Users/tboudreaux/Programing/Albrook/SampleData/Narrators/"
    Series = "/Users/tboudreaux/Programing/Albrook/SampleData/Serise/"

    get_file_structure(Books, Narrators, Series)
    ThomasComputer = Device(deviceName="Dave", deviceType="Darwin",
                            lastIP="10.10.10.10",
                            lastConnect="05-01-2018 12:45:04")

    Thomas = User(firstName = "Thomas", lastName = "Boudreaux",
                  username="tboudreaux", email="thomas@boudreauxmail.com",
                  device=ThomasComputer)
    Artemis = Book.query.first()
    UserBookLink = UserBook(user=Thomas, book=Artemis,
                            lastOpened=datetime.now(), lastLocation=45.3,
                            lastChapter=1)
    db.session.add(ThomasComputer)
    db.session.add(Thomas)
    db.session.add(UserBookLink)
    db.session.commit()
if __name__ == '__main__':
    SampleDataScan()
