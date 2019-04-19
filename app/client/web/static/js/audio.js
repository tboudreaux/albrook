function audioSetup(){
    playerState.playing = false;
    var timer;
    var percent = 0;
    var player = document.getElementById("Player");
    player.addEventListener("play", function(){
        pageState.playing = true;
        let bookID = playerState.getPlayingBook();
        window.timerID = setInterval(postAudioPosition, 10000, bookID);
    });
    player.addEventListener("pause", function(){
        clearInterval(window.timerID);
        postAudioPosition(playerState.getPlayingBook());
        playerState.playing = false;
    });

    $("#Player").bind('ended', function(){
        playNextChapter();
    });
}

function playClick(panelNum){
  if (!playPanelVisible()){
    raisePlayPanel();
  }

  initAudioPlay(panelNum);

  var playButton = $("#togglePlay")
  playButton.html("<i class=\"fa fa-pause\" aria-hidden=\"true\"></i>")

  var coverIMG = $("#playingImage");
  coverIMG.attr("src", getCoverURI(playerState.getPlayingBook(), 200, 200));
}

function initAudioPlay(book_id){
    var source = document.getElementById('audioSource');
    var audio = document.getElementById('Player');

    if (pageState.playing === true){
        postAudioPosition(playerState.getPlayingBook());
        clearInterval(window.timerID);
    }

    var book_id = bookSelector.getBook();
    var currentTrackInfo = getCurrentTrackInfo(book_id);

    if(currentTrackInfo['data'].length == 1){
        var currentChapter = currentTrackInfo['data'][0]['lastChapter'];
        var lastLocation = currentTrackInfo['data'][0]['lastLocation'];

    } else{
        currentChapter = 0;
        lastLocation = "0";
    }

    info = getBookInfo(book_id);
    info = info['data'][0];
    updateCurrentPlayingInfo(info['title'], info['Authors'].join(', '), currentChapter+1);

    source.src = getSyncStream(book_id, currentChapter);

    playerState.setPlayingBook(book_id);
    playerState.setCurrentChapter(currentChapter);

    audio.load();
    audio.currentTime = lastLocation;

    pageState.playing = true;
    audio.play();
}

function playNthChapter(chapter, time=0, offset='start'){
    clearInterval(window.timerID);

    var source = document.getElementById('audioSource');
    var audio = document.getElementById('Player');
    var book_id = playerState.getPlayingBook();

    playerState.setCurrentChapter(chapter)

    source.src = getSyncStream(book_id, playerState.getCurrentChapter());

    audio.load();
    $("#Player").on("loadeddata", function(){
        if (offset === 'start'){
            audio.currentTime = time;
        }
        else if (offset === 'end'){
            audio.currentTime = audio.duration + time
        }
    });
    audio.play();

    postAudioPosition(playerState.getPlayingBook());
    info = getBookInfo(book_id);
    info = info['data'][0];
    updateCurrentPlayingInfo(info['title'], info['Authors'].join(', '), playerState.getCurrentChapter()+1);

    $("#togglePlay").html("<i class=\"fa fa-pause\" aria-hidden=\"true\"></i>")
}

function playNextChapter(time=0, offset='start'){
    let currentChapter = playerState.getCurrentChapter();
    playNthChapter(currentChapter+1, time=time, offset=offset);
}

function playPrevChapter(time=0, offset='start'){
    let currentChapter = playerState.getCurrentChapter();
    playNthChapter(currentChapter-1, time=time, offset=offset);
}

function deltaTime(dt){
    let audio = document.getElementById('Player');
    let duration = audio.duration;
    let currentTime = audio.currentTime;

    // If you need to go to the next chapter
    if (currentTime + dt > duration){
        dt -= duration-currentTime
        playNextChapter(time=dt);
    }

    // If you need to go to the previous chapter
    else if (currentTime + dt < 0){
        dt += currentTime;
        playPrevChapter(time=dt, offset='end');
    }

    // Stay in the same chapter
    else{
        audio.currentTime = currentTime + dt;
    }
}

var advance = function() {
    audio = document.getElementById("Player")
    duration = audio.duration;
    percentCompetedReadout = document.getElementById("percentCompeted");
    var progress = document.getElementById("progress");
    increment = 10/duration
    percent = Math.min(increment * audio.currentTime * 10, 100);
    progress.style.width = percent+'%'
    // let durationFormated = fmtMSS(duration);
    let durationString = duration.toString();
    let durationFormated = durationString.toHHMMSS()
    let completedString = audio.currentTime.toString();
    let completedFormated = completedString.toHHMMSS();
    percentCompetedReadout.innerText = completedFormated + "/" + durationFormated;
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


function updateTrackPosition(fraction){
    audio = document.getElementById("Player");
    audio.currentTime = fraction*audio.duration;
}
