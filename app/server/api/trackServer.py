def getTrackList(engine, book_id):
    conn = engine.connect()
    query = conn.execute("""SELECT Tracks.* FROM Tracks JOIN Books
                            ON Tracks.BookID = Books.UID WHERE
                            Books.UID = {}""".format(book_id))
    result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
    return result


def getChapter(engine, book_id, chapter_id):
    tracks = getTrackList(engine, book_id)
    return {'data' : [tracks['data'][int(chapter_id)]]}

    