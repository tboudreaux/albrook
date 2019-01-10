from datetime import datetime
import app.models as m

nullReturn = {'data': []}

class trackServer:
    @staticmethod
    def getTrackList(book_id):
        r = m.Book.query.filter_by(id=book_id).first()
        if r:
            result = {'data': [x.to_dict() for x in r.tracks]}
        else:
            result = nullReturn
        return result

    @staticmethod
    def getChapter(book_id, chapter_id):
        tracks = trackServer.getTrackList(book_id)
        return {'data' : [tracks['data'][int(chapter_id)]]}

class userBookServer:
    @staticmethod
    def getPickUpInformation(engine, book_id, user_id):
        r = m.UserBook.query.filter_by(bookID=book_id, userID=user_id).all()
        result = {'data': [x.to_dict() for x in r]}
        return result

    @staticmethod
    def updateTrackInfo(user_id, book_id, currentTrack, currentLocation):
        r = m.UserBook.query.filter_by(bookID=book_id, userID=user_id).first()
        if r:
            r.lastOpened = datetime.now()
            r.lastChapter = currentTrack
            r.lastLocation = currentLocation
            return None
        else:
            newUserBookRecord = m.UserBook(userID=user_id, bookID=book_id)
            newUserBookRecord.lastOpened = datetime.now()
            newUserBookRecord.lastChapter = currentTrack
            newUserBookRecord.lastLocation = currentLocation

            return newUserBookRecord
