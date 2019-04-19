window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }


  // TODO: Write code to transition from local play to chromecast play
  //       - Stop local playback
  //       - Resume Chromecast playback where localplayback stoped
  //       - Keep the progress counter and bar going
  //       - transition controls from modifying local audio source to
  //           modifying chromecast remotedplayer
  //       - poll chromecast for position to push to database
  //       - write code to switch back again
  //           - generally it might be good to make this stateful
  // So far
  //       - Chromecast will pick up at the correct audio file
  //       - file will start at the correct time
  //       - file will only be loaded if there is a book currently loaded
window.__onGCastApiAvailable = function(isAvailable){
    if(! isAvailable){
        return false;
    }

    var castContext = cast.framework.CastContext.getInstance();

    castContext.setOptions({
        autoJoinPolicy: chrome.cast.AutoJoinPolicy.ORIGIN_SCOPED,
        receiverApplicationId: chrome.cast.media.DEFAULT_MEDIA_RECEIVER_APP_ID
    });

    var stateChanged = cast.framework.CastContextEventType.CAST_STATE_CHANGED;
    castContext.addEventListener(stateChanged, function(event){
        var castSession = castContext.getCurrentSession();

        if (playerState.getPlayingBook() != null){
          var source = document.getElementById('audioSource');
          var media = new chrome.cast.media.MediaInfo(source.src, 'audio/mp3');
          var request = new chrome.cast.media.LoadRequest(media);

          castSession && castSession
              .loadMedia(request)
              .then(function(){
                  console.log('Success');

                  var player = new cast.framework.RemotePlayer();
                  var playerController = new cast.framework.RemotePlayerController(player);

                  var audio = document.getElementById('Player');
                  console.log('Setting time to: ' + audio.currentTime);
                  playerController.seek(audio.currentTime);

              })
              .catch(function(error){
                  console.log('Error: ' + error);
              });
        }
    });
};