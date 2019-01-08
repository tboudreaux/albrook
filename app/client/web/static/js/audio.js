// TODO -> figure out why the lastLocation is being pushed incorrectly to the DB
//          the same value is getting pushed for all books

jQuery(function(){
    playerState.playing = false;
    var timer;
    var percent = 0;
    var player = document.getElementById("Player");
    player.addEventListener("play", function(){
        pageState.playing = true;
        let bookID = playerState.getPlayingBook();
        let userID = userInfo.userID;
        window.timerID = setInterval(postAudioPosition, 10000, userID, bookID);
    });
    player.addEventListener("pause", function(){
        clearInterval(window.timerID);
        postAudioPosition(userInfo.userID, playerState.getPlayingBook());
        playerState.playing = false;
        clearTimeout(timer);
    });
});

function initAudioPlay(book_id, user_id){
    var source = document.getElementById('audioSource');
    var audio = document.getElementById('Player');

    if (pageState.playing === true){
        postAudioPosition(userInfo.userID, playerState.getPlayingBook());
        clearInterval(window.timerID);
    }

    var book_id = bookSelector.getBook()+1;
    var currentTrackInfo = getCurrentTrackInfo(book_id, user_id);

    if(currentTrackInfo['data'].length == 1){
        var currentChapter = currentTrackInfo['data'][0]['LastChapter'];
        var lastLocation = currentTrackInfo['data'][0]['LastLocation'];

    } else{
        currentChapter = 0;
        lastLocation = "0";
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

function playNextChapter(){
    // TODO -> Add extra field to UsersBooks: finished
    // TODO -> Add system for dealing with when book is finished
    var source = document.getElementById('audioSource');
    var audio = document.getElementById('Player');
    var book_id = playerState.getPlayingBook()

    playerState.incrimentCurrentChapter();

    source.src = getSyncStream(book_id, playerState.getCurrentChapter());

    audio.load();
    audio.currentTime = 0;
    audio.play();

    postAudioPosition(userInfo.userID, playerState.getPlayingBook());
    updateCurrentPlayingInfo(info.titles[book_id-1], info.authors[book_id-1], playerState.getCurrentChapter()+1);
}

function playPrevChapter(){
    // TODO -> Add extra field to UsersBooks: finished
    // TODO -> Add system for dealing with when book is finished
    var source = document.getElementById('audioSource');
    var audio = document.getElementById('Player');
    var book_id = playerState.getPlayingBook()

    playerState.decrimentCurrentChapter();

    source.src = getSyncStream(book_id, playerState.getCurrentChapter());

    audio.load();
    audio.currentTime = 0;
    audio.play();

    postAudioPosition(userInfo.userID, playerState.getPlayingBook());
    updateCurrentPlayingInfo(info.titles[book_id-1], info.authors[book_id-1], playerState.getCurrentChapter()+1);
}

var advance = function() {
    audio = document.getElementById("Player")
    duration = audio.duration;
    percentCompetedReadout = document.getElementById("percentCompeted");
    var progress = document.getElementById("progress");
    var slider = document.getElementById("progressSlider");
    increment = 10/duration
    percent = Math.min(increment * audio.currentTime * 10, 100);
    progress.style.width = percent+'%'
    let durationFormated = fmtMSS(duration);
    let completedFormated = fmtMSS(audio.currentTime);
    percentCompetedReadout.innerText = completedFormated.slice(0, 5) + "/" + durationFormated.slice(0, 5);

    slider.style.position = 'absolute';
    slider.style.left = percent+ '%';
}


function togglePlay (e) {
  e = e || window.event;
  var btn = e.target;
  var player = document.getElementById("Player");
  if (!player.paused) {
    btn.classList.remove('active');
    player.pause();
    pageState.playing = false;
  } else {
    btn.classList.add('active');
    player.play();
    pageState.playing = true;
  }
}

function handelMove(e){
    var slider = document.getElementById('progressSlider');
    if (pageState.playing === true){
        slider.style.position = 'absolute';
        slider.style.left = e.clientX + 'px';
    }
}

function updateTrackPosition(fraction){
    audio = document.getElementById("Player");
    audio.currentTime = fraction*audio.duration;
}

