function addBookClickListner(){
  Books = getBooks();
  for (let book of Books['data']){
    let i = book.id;
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

      initAudioPlay(panelNum);

      var playButton = $("#togglePlay")
      playButton.html("<i class=\"fa fa-pause\" aria-hidden=\"true\"></i>")


      var coverIMG = $("#playingImage");
      coverIMG.attr("src", getCoverURI(playerState.getPlayingBook(), 200, 200));

    }, false);
  }
}

function addAuthorClickListner(){
  Authors = getAuthors();
  for (let author of Authors['data']){
    let i = author.id;
    document.getElementById("author_panel_"+i).addEventListener("click", function(e) {
      pageState.displayingInfo = 'author';
      if (e.target === this){
        smartInfo = smartInfoShow(e, prevPanel, true, false);
      }else{
        smartInfo = smartInfoShow(e, prevPanel, false, Hide);
      }
      prevPanel = smartInfo.panelNum;
      Hide = smartInfo.Hide;
    }, false);
  }
}
