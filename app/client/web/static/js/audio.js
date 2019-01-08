// TODO -> figure out why the lastLocation is being pushed incorrectly to the DB
//          the same value is getting pushed for all books

jQuery(function(){
    var timerID;
    playerState.playing = false;
    document.getElementById("Player").addEventListener("play", function(){
        pageState.playing = true;
        let bookID = playerState.getPlayingBook();
        let userID = userInfo.userID;
        timerID = setInterval(postAudioPosition, 10000, userID, bookID);
    });
    document.getElementById("Player").addEventListener("pause", function(){
        if (pageState.playing){
            clearInterval(timerID);
        }
        playerState.playing = false;
    });
});

function initAudioPlay(book_id, user_id){
    var source = document.getElementById('audioSource');
    var audio = document.getElementById('Player');

    var book_id = bookSelector.getBook()+1;
    var currentTrackInfo = getCurrentTrackInfo(book_id, user_id);
    if(currentTrackInfo['data'].length == 1){
        var currentChapter = currentTrackInfo['data'][0]['LastChapter'];
        var lastLocation = currentTrackInfo['data'][0]['LastLocation'];

    } else{
        currentChapter = 0;
        lastLocation = "0";
    }      

    if (pageState.playing){
        postAudioPosition(userInfo.userID, playerState.getPlayingBook());
    }

    updateCurrentPlayingInfo(info.titles[book_id-1], info.authors[book_id-1], currentChapter+1);

    source.src = getSyncStream(book_id, currentChapter);

    playerState.setPlayingBook(book_id);
    playerState.setCurrentChapter(currentChapter);

    audio.load();
    audio.currentTime = lastLocation;

    pageState.playing = true;
    audio.play();
}

