jQuery(function(){
    var timerID;
    pageState.playing = false;
    document.getElementById("Player").addEventListener("play", function(){
        pageState.playing = true;
        let bookID = pageState.getPlayingBook();
        let userID = userInfo.userID;
        timerID = setTimeout(putAudioPosition, 30, bookID, userID);
    });
    document.getElementById("Player").addEventListener("pause", function(){
        if (pageState.playing){
            clearTimeout(timerId);
        }
        pageState.playing = false;
    });
});

