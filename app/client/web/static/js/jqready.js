jQuery(function(){
    $("#playPanel").hide();
    pageState.infoState = false;
    pageState.playPanelState = false;
    pageState.sideBarState = false;
    userInfo.userID = 0;
    pageState.setPlayingBook(1);
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
    
})