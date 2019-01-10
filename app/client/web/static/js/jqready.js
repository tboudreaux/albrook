jQuery(function(){
    $("#playPanel").hide();
    pageState.infoState = false;
    pageState.playPanelState = false;
    pageState.sideBarState = false;
    pageState.playing = false;
    userInfo.userID = 0;
});

jQuery(function(){
  var playButton = document.getElementById("#playPanelShowControlContainer");
  $("#playPanelShowControl").addClass('up');
  $("#playPanelShowControl").click(function(e){
    togglePlayPanel();
  });
});

jQuery(function(){
    for (i = 1; i < numBooks+1; i++){
      document.getElementById("book_panel_"+i).addEventListener("click", function(e) {
        pageState.displayingInfo = 'book';
        if (e.target === this){
          smartInfo = smartInfoShow(e, prevPanel, true, false);
        }else{
          smartInfo = smartInfoShow(e, prevPanel, false, Hide);
        }
        prevPanel = smartInfo.panelNum;
        Hide = smartInfo.Hide;
      }, false);
      document.getElementById("rig-text-"+i).addEventListener("mousedown", function(e){
        pageState.displayingInfo = 'book';
        var panelNum = GetPanelNumber(e.path);
        $("#rig-text-"+panelNum).html("<i class=\"fa fa-play-circle\"></i>");
      }, false);
      document.getElementById("rig-text-"+i).addEventListener("mouseup", function(e){
        pageState.displayingInfo = 'book'
        var panelNum = GetPanelNumber(e.path);
        $("#rig-text-"+panelNum).html("<i class=\"fa fa-play-circle-o\"></i>");
        smartInfo = smartInfoShow(e, prevPanel, true, false);
        prevPanel = smartInfo.panelNum;
        Hide = smartInfo.Hide;

        if (!playPanelVisible()){
          raisePlayPanel();
        }

        initAudioPlay(panelNum, userInfo.userID);

        var playButton = $("#togglePlay")
        playButton.html("<i class=\"fa fa-pause\" aria-hidden=\"true\"></i>")


        console.log('HERE');
        var coverIMG = $("#playingImage");
        coverIMG.attr("src", getCoverURI(playerState.getPlayingBook(), 200, 200));

      }, false);
    }
});

jQuery(function(){
  var sideBar = $("#sideBar");
  var sideBarToggle = $("#sideBarToggle");

  sideBarToggle.click(function(e){
    toggleSideBar();
  });
});

jQuery(function(){
  var authorLink = $("#infoAuthor");
  var infoText = $("#infoText");
  authorLink.click(function(e){
    infoText.fadeOut("slow", function() {
      showAuthorInfo(e.target.innerText);
    });
    infoText.fadeIn("slow");
    pageState.displayingInfo = "author";
  });

});

jQuery(function(){
  $("#Player").bind('ended', function(){
      playNextChapter();
  });
});

jQuery(function(){
  var playButton = $("#togglePlay");
  playButton.click(function(e){
    if (pageState.playing == true){
      playButton.html("<i class=\"fa fa-pause\" aria-hidden=\"true\"></i>")
    }else{
      playButton.html("<i class=\"fa fa-play\" aria-hidden=\"true\"></i>")
    }
  });
});

jQuery(function(){
  var progress = $("#shadowProgress");
  progress.click(function(e){
    var offsetX = $(this).offset().left
    var posX = e.pageX - offsetX
    var totalWidth = progress.width();
    updateTrackPosition(posX/totalWidth);
  });
});

jQuery(function(){
  var logOut = $("#logOut");
  logOut.click(function(e){
    doLogout();
  })
})
