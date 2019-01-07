// Function to play current audio when old play button was clicked
jQuery(function(){
  var playPanel = $("#playPanel");
  playPanel.hide();
  $("#playButton").click(function(e){
    var audio = document.getElementById('Player');
    var source = document.getElementById('audioSource');
    if (!playPanelVisible()){
      raisePlayPanel();

      $("#playButton").html("<i class=\"fa fa-stop\"></i>");

      var book_id = bookSelector.getBook()+1;
      var currentTrackInfo = getCurrentTrackInfo(book_id, 0);
      if(currentTrackInfo['data'].length == 1){
        var currentChapter = currentTrackInfo['data'][0]['LastChapter'];
        var lastLocation = currentTrackInfo['data'][0]['LastLocation'];
      
      } else{
        currentChapter = 0;
        lastLocation = "00:00:00";
      }

      updateCurrentPlayingInfo(info.titles[book_id-1], info.authors[book_id-1], currentChapter+1);

      source.src = getSyncStream(book_id, currentChapter);
      audio.load();
      audio.currentTime = getSecondsFromTimestring(lastLocation);
      // audio.play();
    }
    else{

      $("#playButton").html("<i class=\"fa fa-play\"></i>");

      audio.pause();
    }
  });
});