var bookSelector = (function(){
    var currentBook;
    var pub = {};

    pub.ChangeBook = function(newBook){
        currentBook = newBook;
    }

    pub.getBook = function(){
        return currentBook;
    }

    return pub;
}());

var playerState = (function(){
    var playingInfo = {};
    var pub = {};

    pub.setPlayingBook = function(bookID){
        playingInfo.bookID = bookID;
    }

    pub.getPlayingBook = function(){
        return playingInfo.bookID;
    }

    pub.setCurrentChapter = function(currentChapter){
        playingInfo.currentChapter = currentChapter;
    }

    pub.getCurrentChapter = function(currentChapter){
        return playingInfo.currentChapter;
    }

    return pub;

}());

var pageState = {};

var userInfo = (function(){
    var userID;
});