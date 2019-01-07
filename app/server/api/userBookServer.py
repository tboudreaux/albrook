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
    conn.execute("""UPDATE UsersBooks SET LastLocation = "{}",
                    LastChapter = {} WHERE UsersBooks.BookID = {} and
                    UsersBooks.UserID = {}""".format(currentLocation,
                                                    currentTrack,
                                                    book_id, user_id))