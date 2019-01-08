from datetime import datetime

def getPickUpInformation(engine, book_id, user_id):
    conn = engine.connect()
    query = conn.execute("""SELECT UsersBooks.LastChapter,
                            UsersBooks.LastLocation FROM Books
                            JOIN UsersBooks ON Books.UID = UsersBooks.BookID
                            JOIN Users ON UsersBooks.UserID = Users.UID
                            WHERE UsersBooks.BookID = {} AND
                            UsersBooks.UserID = {}""".format(book_id, user_id))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    return result

def updateTrackInfo(engine, user_id, book_id, currentTrack, currentLocation):
    conn = engine.connect()
    exists = conn.execute("""SELECT COUNT(*) AS NUM FROM UsersBooks
                             WHERE UsersBooks.BookID = {} and
                             UsersBooks.UserID = {}""".format(book_id, user_id))
    result = {'data': [dict(zip(tuple(exists.keys()), i)) for i in exists.cursor]}
    if result['data'][0]['NUM'] == 1:
        LastOpened = datetime.now().strftime("%d-%m-%Y %H:%M")
        conn.execute("""UPDATE UsersBooks SET LastLocation = "{}",
                        LastChapter = {}, LastOpened = "{}" WHERE UsersBooks.BookID = {} and
                        UsersBooks.UserID = {}""".format(currentLocation,
                                                        currentTrack, LastOpened,
                                                        book_id, user_id))
    else:
        LastOpened = datetime.now().strftime("%d-%m-%Y %H:%M")
        conn.execute("""INSERT INTO UsersBooks (UserID, BookID, LastOpened,
                        LastLocation, LastChapter) VALUES ({}, {},
                        \"{}\", \"{}\", \"{}\")""".format(user_id, book_id,
                                                          LastOpened, currentLocation,
                                                          currentTrack))