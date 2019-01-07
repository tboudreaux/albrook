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

var pageState = (function(){
    var infoState;
    var sideBarState;
    var playPanelState;
    var displayingInfo;
    var playingInfo = {};
    var playing;

    var pub = {}

    pub.setPlayingBook = function(bookID){
        playingInfo.bookID = bookID;
    }

    pub.getPlayingBook = function(){
        return playingInfo.bookID
    }

    return pub;
}());

var userInfo = (function(){
    var userID;
});