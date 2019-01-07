import os
import sqlite3
from sqlite3 import Error as SQLITEERROR
from utils import sort_nicely, clear_lists
import json

IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'gif', 'tiff']

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except SQLITEERROR as e:
        print(e)


def generate_table(conn):
    mkAuthorTableQuery = """CREATE TABLE IF NOT EXISTS Authors (
    UID INT PRIMARY KEY,
    FirstName VARCHAR(128) NOT NULL,
    MiddleName VARCHAR(128),
    LastName VARCHAR(128),
    Biography TEXT,
    ProfileImage VARCHAR(1024),
    Nationality VARCHAR(256)
    ); """
    mkNarratorsTableQuery = """CREATE TABLE IF NOT EXISTS Narrators (
    UID INT PRIMARY KEY,
    FirstName VARCHAR(128) NOT NULL,
    MiddleName VARCHAR(128),
    LastName VARCHAR(128),
    Biography TEXT,
    ProfileImage VARCHAR(4096),
    Nationality VARCHAR(256)
    ); """
    mkGenresTableQuery = """CREATE TABLE IF NOT EXISTS Genres (
    UID INT PRIMARY KEY,
    Name VARCHAR(128) NOT NULL,
    Description TEXT
    ); """
    mkDeviceTableQuery = """CREATE TABLE IF NOT EXISTS Devices (
    UID INT PRIMARY KEY,
    DeviceName VARCHAR(32) NOT NULL,
    LastIP VARCHAR(32) NOT NULL,
    LastConnect  VARCHAR(19) NOT NULL,
    DeviceType VARCHAR(32)
    ); """
    mkTagsTableQuery = """CREATE TABLE IF NOT EXISTS Tags (
    UID INT PRIMARY KEY,
    Name VARCHAR(64) UNIQUE NOT NULL 
    ); """
    mkSeriesTableQuery = """CREATE TABLE IF NOT EXISTS Series (
    UID INT PRIMARY KEY,
    Name VARCHAR(64) UNIQUE NOT NULL,
    Description TEXT
    ); """
    mkUserTableQuery = """CREATE TABLE IF NOT EXISTS Users (
    UID INT PRIMARY KEY,
    FirstName VARCHAR(128) NOT NULL,
    LastName VARCHAR(128) NOT NULL,
    Email VARCHAR(256),
    Biography TEXT,
    Username VARCHAR(128) UNIQUE NOT NULL,
    Password VARCHAR(4096) NOT NULL,
    LastDevice INT NOT NULL,
    ProfileImage BLOB,
    FOREIGN KEY (LastDevice) REFERENCES Devices (UID)
    ); """
    mkBookTableQuery = """CREATE TABLE IF NOT EXISTS Books (
    UID INT PRIMARY KEY,
    Title VARCHAR(128) NOT NULL,
    PublicationDate VARCHAR(10),
    Description TEXT,
    Chapters INT NOT NULL,
    Cover VARCHAR(1024),
    HasFilm BOOLEAN
    ); """
    mkAuthorsBooksTableQuery = """CREATE TABLE IF NOT EXISTS AuthorsBooks (
    BookID INT,
    AuthorID INT,
    PRIMARY KEY (BookID, AuthorID),
    FOREIGN KEY (BookID) REFERENCES Books (UID),
    FOREIGN KEY (AuthorID) REFERENCES Authors (UID)
    ); """
    mkNarratorsBooksTableQuery = """CREATE TABLE IF NOT EXISTS NarratorsBooks (
    BookID INT,
    NarratorID INT,
    PRIMARY KEY (BookID, NarratorID),
    FOREIGN KEY (BookID) REFERENCES Books (UID),
    FOREIGN KEY (NarratorID) REFERENCES Narrators (UID)
    ); """
    mkGenresBooksTableQuery = """CREATE TABLE IF NOT EXISTS GenresBooks (
    BookID INT,
    GenreID INT,
    PRIMARY KEY (BookID, GenreID),
    FOREIGN KEY (BookID) REFERENCES Books (UID),
    FOREIGN KEY (GenreID) REFERENCES Genres (UID)
    ); """
    mkTagsBooksTableQuery = """CREATE TABLE IF NOT EXISTS TagsBooks (
    BookID INT,
    TagID INT,
    PRIMARY KEY (BookID, TagID),
    FOREIGN KEY (BookID) REFERENCES Books (UID),
    FOREIGN KEY (TagID) REFERENCES Tags (UID)
    ); """
    mkSeriesBooksTableQuery = """CREATE TABLE IF NOT EXISTS SeriesBooks (
    BookID INT,
    SeriesID INT,
    PRIMARY KEY (BookID, SeriesID),
    FOREIGN KEY (BookID) REFERENCES Books (UID),
    FOREIGN KEY (SeriesID) REFERENCES Series (UID)
    ); """
    mkUsersBooksTableQuery = """CREATE TABLE IF NOT EXISTS UsersBooks (
    UserID INT NOT NULL,
    BookID INT NOT NULL,
    LastOpened VARCHAR(19) NOT NULL,
    LastLocation VARCHAR(19) NOT NULL,
    LastChapter INT NOT NULL,
    PRIMARY KEY (UserID, BookID),
    FOREIGN KEY (UserID) REFERENCES Users (UID),
    FOREIGN KEY (BookID) REFERENCES Books (UID)
    ); """
    mkTracksTableQuery = """CREATE TABLE IF NOT EXISTS Tracks (
    UID INT PRIMARY KEY,
    FilePath TEXT NOT NULL,
    BookID INT NOT NULL,
    Chapter Int NOT NULL,
    FOREIGN KEY (BookID) REFERENCES Books (UID)
    ); """

    create_table(conn, mkAuthorTableQuery)
    create_table(conn, mkNarratorsTableQuery)
    create_table(conn, mkGenresTableQuery)
    create_table(conn, mkDeviceTableQuery)
    create_table(conn, mkTagsTableQuery)
    create_table(conn, mkSeriesTableQuery)
    create_table(conn, mkUserTableQuery)
    create_table(conn, mkBookTableQuery)
    create_table(conn, mkAuthorsBooksTableQuery)
    create_table(conn, mkNarratorsBooksTableQuery)
    create_table(conn, mkGenresBooksTableQuery)
    create_table(conn, mkTagsBooksTableQuery)
    create_table(conn, mkSeriesBooksTableQuery)
    create_table(conn, mkUsersBooksTableQuery)
    create_table(conn, mkTracksTableQuery)

    conn.commit()


def build_db(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
    except SQLITEERROR as e:
        print(e)

    return conn, conn.cursor()


def file_is_of_type(filePath, fileType):
    if filePath.split('.')[1] == fileType:
        return True
    else:
        return False
        

def get_file_type(filePath):
    return filePath.split('.')[-1]


def get_table_uid(conn, table):
    query = "SELECT COUNT(*) FROM {}".format(table)
    c = conn.cursor()
    c.execute(query)
    count = c.fetchall()
    uid = count[0][0] + 1
    return uid


def insert_into_table(conn, UID, table, columns, values):
    formatedValues = ['"{}"'.format(x) if type(x) == str else str(x) for x in values]
    c = conn.cursor()
    columns = "(UID, {})".format(", ".join(columns))
    insertValues = "({}, {})".format(UID, ", ".join(formatedValues))
    Query = "INSERT INTO {} {} VALUES {}".format(table, columns, insertValues)
    c.execute(Query)
    conn.commit()


def insert_into_link_table(conn, UIDNames, UIDs, table):
    c = conn.cursor()
    UIDs = [str(x) for x in UIDs]
    columns = "({})".format(", ".join(UIDNames))
    insertValues = "({})".format(", ".join(UIDs))
    Query = "INSERT INTO {} {} VALUES {}".format(table, columns, insertValues)
    c.execute(Query)
    conn.commit()


def is_author(conn, FirstName, LastName):
    c = conn.cursor()
    query = 'SELECT COUNT(UID) FROM Authors WHERE FirstName=="{}" and LastName=="{}"'.format(FirstName, LastName)
    c.execute(query)
    count = c.fetchall()[0][0]
    if count != 0:
        return True
    else:
        return False

def get_author_id(conn, FirstName, LastName):
    if is_author(conn, FirstName, LastName):
        c = conn.cursor()
        query = 'SELECT UID FROM Authors WHERE FirstName=="{}" and LastName=="{}"'.format(FirstName, LastName)
        c.execute(query)
        uid = c.fetchall()[0][0]
        return uid


def is_genre(conn, genre):
    c = conn.cursor()
    query = 'SELECT COUNT(UID) FROM Genres WHERE Name=="{}"'.format(genre)
    c.execute(query)
    count = c.fetchall()[0][0]
    if count != 0:
        return True
    else:
        return False

def get_genre_id(conn, genre):
    if is_genre(conn, genre):
        c = conn.cursor()
        query = 'SELECT UID FROM Genres WHERE Name=="{}"'.format(genre)
        c.execute(query)
        uid = c.fetchall()[0][0]
        return uid


def is_narrator(conn, FirstName, LastName):
    c = conn.cursor()
    query = 'SELECT COUNT(UID) FROM Narrators WHERE FirstName=="{}" and LastName=="{}"'.format(FirstName, LastName)
    c.execute(query)
    count = c.fetchall()[0][0]
    if count != 0:
        return True
    else:
        return False

def get_narrator_id(conn, FirstName, LastName):
    if is_narrator(conn, FirstName, LastName):
        c = conn.cursor()
        query = 'SELECT UID FROM Narrators WHERE FirstName=="{}" and LastName=="{}"'.format(FirstName, LastName)
        c.execute(query)
        uid = c.fetchall()[0][0]
        return uid

def is_series(conn, series):
    c = conn.cursor()
    query = 'SELECT COUNT(UID) FROM Series WHERE Name="{}"'.format(series)
    c.execute(query)
    count = c.fetchall()[0][0]
    if count != 0:
        return True
    else:
        return False


def get_series_id(conn, series):
    if is_series(conn, series):
        c = conn.cursor()
        query = 'SELECT UID FROM Series WHERE Name="{}"'.format(series)
        c.execute(query)
        uid = c.fetchall()[0][0]
        return uid


def is_tag(conn, tag):
    c = conn.cursor()
    query = 'SELECT COUNT(UID) FROM Tags WHERE Name="{}"'.format(tag)
    c.execute(query)
    count = c.fetchall()[0][0]
    if count != 0:
        return True
    else:
        return False

def get_tag_id(conn, tag):
    if is_tag(conn, tag):
        c = conn.cursor()
        query = 'SELECT UID FROM Tags WHERE Name="{}"'.format(tag)
        c.execute(query)
        uid = c.fetchall()[0][0]
        return uid


def add_author(conn, Author, pathToAuthor):
    FullName = Author.split(' ')
    FirstName = FullName[0]
    LastName = FullName[-1]
    if not is_author(conn, FirstName, LastName):
        AuthorID = get_table_uid(conn, 'Authors')
        columns = ['FirstName', 'LastName']
        values = [FirstName, LastName]
        if len(FullName) > 2:
            columns.append('MiddleName')
            values.append(FullName[1])
        files = os.listdir(pathToAuthor)
        if 'author.json' in files:
            with open(os.path.join(pathToAuthor, 'author.json')) as f:
                data = json.load(f)
            bio = data['Biography']
            nat = data['Nationality']
            bio = bio.replace('"', '""')
            bio = bio.replace("'", "''")
            bio = bio.replace('\\n', '\n')
            columns.extend(['Biography', 'Nationality'])
            values.extend([bio, nat])
        for file in files:
            if "portrait" == file.split('.')[0]:
                if get_file_type(os.path.join(pathToAuthor, file)).lower() in IMAGE_TYPES:
                    columns.append('ProfileImage')
                    values.append('{}'.format(os.path.join(pathToAuthor, file)))

        values, columns = clear_lists(values, columns)
        insert_into_table(conn, AuthorID, "Authors", columns, values)
    else:
        AuthorID = get_author_id(conn, FirstName, LastName)
    return AuthorID


def add_tracks(conn, pathToBook, book):
    chapters = os.listdir(pathToBook)
    chapters = [x for x in chapters if file_is_of_type(x, 'mp3')]
    for chapterNum, chapter in enumerate(sort_nicely(chapters)):
        trackID = get_table_uid(conn, 'Tracks')
        columns = ['FilePath', 'BookID', 'Chapter']
        values = [os.path.join(pathToBook, chapter), book, chapterNum]
        insert_into_table(conn, trackID, "Tracks", columns, values)
    return len(chapters)


def add_genre(conn, genre):
    if not is_genre(conn, genre):
        genreID = get_table_uid(conn, 'Genres')
        columns = ["Name"]
        values = [genre]
        insert_into_table(conn, genreID, "Genres", columns, values)
    else:
        genreID = get_genre_id(conn, genre)
    return genreID


def add_narrator(conn, narrator, narratorPath):
    orig = narrator
    narrator = narrator.replace(' ', '')
    narrator = narrator.replace('.', '')
    if os.path.exists(os.path.join(narratorPath, '{}.json'.format(narrator))):
        with open(os.path.join(narratorPath, '{}.json'.format(narrator))) as f:
            data = json.load(f)
        columns = ['FirstName', 'MiddleName', 'LastName',
                   'Biography', 'ProfileImage', 'Nationality']
        bio = data['Biography']
        bio = bio.replace('"', '""')
        bio = bio.replace("'", "''")
        bio = bio.replace('\\n', '\n')
        FirstName = data['FirstName']
        LastName = data['LastName']
        values = [FirstName, data['MiddleName'],
                  LastName, bio, data['ProfileImage'],
                  data['Nationality']]
    else:
        FullName = orig.split(' ')
        columns = ['FirstName', 'LastName']
        FirstName = FullName[0]
        LastName = FullName[-1]
        values = [FirstName, LastName]
        if len(FullName) > 2:
            columns.append('MiddleName')
            values.append(FullName[1])
    if not is_narrator(conn, FirstName, LastName):
        NarratorID = get_table_uid(conn, 'Narrators')
        values, columns = clear_lists(values, columns)
        insert_into_table(conn, NarratorID, "Narrators", columns, values)
    else:
        NarratorID = get_narrator_id(conn, FirstName, LastName)
    return NarratorID


def add_series(conn, series, seriesPath):
    Name = series
    series = series.replace(' ', '')
    if os.path.exists(os.path.join(seriesPath, '{}.json'.format(series))):
        with open(os.path.join(seriesPath, '{}.json'.format(series))) as f:
            data = json.load(f)
        columns = ['Name', 'Description']
        desc = data['Description']
        desc = desc.replace('"', '""')
        desc = desc.replace("'", "''")
        desc = desc.replace('\\n', '\n')
        Name = data['Name']
        values = [Name, desc]
    else:
        columns = ['Name']
        values = [Name]
    if not is_series(conn, Name):
        SeriesID = get_table_uid(conn, 'Series')
        values, columns = clear_lists(values, columns)
        insert_into_table(conn, SeriesID, "Series", columns, values)
    else:
        SeriesID = get_series_id(conn, Name)
    return SeriesID


def add_tag(conn, tag):
    if not is_tag(conn, tag):
        TagID = get_table_uid(conn, 'Tags')
        columns = ['Name']
        values = [tag]
        insert_into_table(conn, TagID, "Tags", columns, values)
    else:
        TagID = get_tag_id(conn, tag)
    return TagID


def add_book(conn, pathToBook, files, narratorPath, seriesPath):    
    BookID = get_table_uid(conn, 'Books')
    Chapters = add_tracks(conn, pathToBook, BookID)
    rootSplit = pathToBook.split('/')

    if "book.json" in files:

        with open(os.path.join(pathToBook, "book.json")) as f:
            data = json.load(f)

        fields = data.keys()
        if 'Title' in fields:
            Title = data['Title']
        else:
            Title = rootSplit[-1]

        columns = ["Title", "Chapters"]
        values = [Title, Chapters]

        if "Authors" in fields:
            authors = data['Authors']
            AIDs = list()
            for author in authors:
                AIDs.append(add_author(conn, author, '/'.join(rootSplit[:-1])))
        else:
            Author = rootSplit[-2]
            AuthorID = add_author(conn, Author, '/'.join(rootSplit[:-1]))
            AIDs = [AuthorID]

        AColumns = ['BookID', 'AuthorID']
        for AuthorID in AIDs:
            AValues = [BookID, AuthorID]
            insert_into_link_table(conn, AColumns, AValues, "AuthorsBooks")

        if 'Description' in fields:
            Desc = data['Description']
            Desc = Desc.replace('"', '""')
            Desc = Desc.replace("'", "''")
            columns.append("Description")
            values.append(Desc)

        if 'PublicationDate' in fields:
            PublicationDate = data['PublicationDate']
            columns.append("PublicationDate")
            values.append(PublicationDate)

        if 'Narrators' in fields:
            Narrators = data['Narrators']
            NIDs = list()
            for narrator in Narrators:
                NIDs.append(add_narrator(conn, narrator, narratorPath))
            NColumns = ['BookID', 'NarratorID']
            for NarratorID in NIDs:
                NValues = [BookID, NarratorID]
                insert_into_link_table(conn, NColumns, NValues, "NarratorsBooks")

        if "Genres" in fields:
            Genres = data['Genres']
            GIDs = list()
            for genre in Genres:
                GIDs.append(add_genre(conn, genre))
            GColumns = ['BookID', 'GenreID']
            for GenreID in GIDs:
                GValues = [BookID, GenreID]
                insert_into_link_table(conn, GColumns, GValues, "GenresBooks")

        if "Series" in fields:
            Series = data['Series']
            SIDs = list()
            for series in Series:
                SIDs.append(add_series(conn, series, seriesPath))
            SColumns = ['BookID', 'SeriesID']
            for SeriesID in SIDs:
                SValues = [BookID, SeriesID]
                insert_into_link_table(conn, SColumns, SValues, "SeriesBooks")

        if "Tags" in fields:
            Tags = data['Tags']
            TIDs = list()
            for tag in Tags:
                TIDs.append(add_tag(conn, tag))
            TColumns = ['BookID', 'TagID']
            for TagID in TIDs:
                TValues = [BookID, TagID]
                insert_into_link_table(conn, TColumns, TValues, "TagsBooks")


    for file in files:
        if "cover" == file.split('.')[0]:
            if get_file_type(os.path.join(pathToBook, file)).lower() in IMAGE_TYPES:
                columns.append('Cover')
                values.append('{}'.format(os.path.join(pathToBook, file)))

    insert_into_table(conn, BookID, "Books", columns, values)


def get_file_structure(conn, Books, Narrators, Series):
    for i, (Books, dirs, files) in enumerate(os.walk(Books, topdown=False)):
        bookfound = False
        for file in files:
            if file_is_of_type(file, 'mp3'):
                bookfound = True
        if bookfound:
            add_book(conn, Books, files, Narrators, Series)


if __name__ == '__main__':
    Books = "/Users/tboudreaux/Programing/Albrook/SampleData/Audiobooks/"
    Narrators = "/Users/tboudreaux/Programing/Albrook/SampleData/Narrators/"
    Series = "/Users/tboudreaux/Programing/Albrook/SampleData/Serise/"

    conn, c = build_db('albrook.db')
    generate_table(conn)
    get_file_structure(conn, Books, Narrators, Series)
    conn.close()
