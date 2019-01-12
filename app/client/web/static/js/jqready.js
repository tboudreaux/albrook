jQuery(function(){
  pageState.infoState = false;
  pageState.playPanelState = false;
  pageState.sideBarState = false;
  pageState.playing = false;
});

function playPanelSetup(){
    $("#playPanel").hide();

    $("#playPanelShowControl").addClass('up');
    $("#playPanelShowControl").click(function(e){
      togglePlayPanel();
    });

    var playButton = $("#togglePlay");
    playButton.click(function(e){
      if (pageState.playing == true){
        playButton.html("<i class=\"fa fa-pause\" aria-hidden=\"true\"></i>")
      }else{
        playButton.html("<i class=\"fa fa-play\" aria-hidden=\"true\"></i>")
      }
    });

    var progress = $("#shadowProgress");
    progress.click(function(e){
      var offsetX = $(this).offset().left
      var posX = e.pageX - offsetX
      var totalWidth = progress.width();
      updateTrackPosition(posX/totalWidth);
    });
}

function sideBarSetup(){
  var sideBar = $("#sideBar");
  var sideBarToggle = $("#sideBarToggle");

  sideBarToggle.click(function(e){
    toggleSideBar();
  });
}

function authorInfoSetup(){
  var authorLink = $("#infoAuthor");
  var infoText = $("#infoText");
  authorLink.click(function(e){
    infoText.fadeOut("slow", function() {
      showAuthorInfoName(e.target.innerText);
    });
    infoText.fadeIn("slow");
    pageState.displayingInfo = "author";
  });

}
