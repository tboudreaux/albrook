function postAudioPosition(book_id){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open('POST', "/Book/id:" + book_id + "/currentTrack", true);  // true : asynchrone false: synchrone
    xmlHttp.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    var currentLocation = document.getElementById("Player").currentTime;
    var currentChapter = playerState.getCurrentChapter();

    var data = JSON.stringify({"currentLocation": currentLocation, "currentChapter": currentChapter});
    xmlHttp.send(data);
}
