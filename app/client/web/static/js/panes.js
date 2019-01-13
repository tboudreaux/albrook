function toggleinfoPane(id, Hide) {
  let page = getActivePageID();

  if (page == "bookPage"){
    setBookInfo(id);
    bookSelector.ChangeBook(id);
  }else if (page == "authorPage") {
    setAuthorInfo(id);
  }

  var infoPane = $('#infoPane');
  if (!infoPane.hasClass('visible')){
    extendInfoPane();
  }
  else {
    if (Hide === true){
      retractInfoPane();
    }
  }
}

function setBookInfo(book_id){
  info = getBookInfo(book_id);
  if (info){
    info = info['data'][0]
    $("#infoTitle").text(info['title']);
    $("#infoSecondaryA").text(info['Authors'].join(', '));
    $("#infoSecondaryB").text(info['Narrators'].join(', '));
    $("#infoBlock").text(info['description']);

    // var coverURI = getCoverURI(book_id, 300, 300);
    // document.getElementById('infoPhoto').src = coverURI;

    let books = getBooksByAuthorByBook(book_id);
    let infoPhotoRig = $("#infoPhotoRig");
    infoPhotoRig.empty();
    for (let book of books['data']){
      coverURI = getCoverURI(book.id, 300, 300);
      infoPhotoRig.append(`
        <li>
            <div class=\"rig-cell\" id=\"books_by_same_author_book_panel_`+ book.id +`\">
              <img class=\"rig-img\" src=\"` + coverURI + `\">
              <span class=\"rig-overlay\"></span>
            </div>
        </li>`);

        let cell = $("#books_by_same_author_book_panel_"+book.id);
        cell.click(function(e){
          clickListner(e, "books_by_same_author_book_panel_", "book");
        });
    }
  }
}

function setAuthorInfo(author_id){
  authorInfo = getAuthorInfo(author_id);
  if (authorInfo){
    let authorName = authorInfo['data'][0].firstName + " " + authorInfo['data'][0].lastName;
    if (authorInfo['data'][0].middleName !== null){
        authorName = authorName.replace(' ', " " + authorInfo['data'][0].middleName + " ") ;
    }

    $("#infoTitle").text(authorName);
    $("#infoSecondaryA").text(authorInfo['data'][0].nationality);
    $("#infoSecondaryB").text("");
    $("#infoBlock").text(authorInfo['data'][0].biography);

    // var portraitURI = getAuthorPortaitURI(authorInfo['data'][0]['id'], 300, 300);
    // document.getElementById('infoPhoto').src = portraitURI;

    let books = getAuthorBooks(author_id);
    let infoPhotoRig = $("#infoPhotoRig");
    infoPhotoRig.empty();
    for (let book of books['data']){
      coverURI = getCoverURI(book.id, 300, 300);
      infoPhotoRig.append(`
        <li>
            <div class=\"rig-cell\" id=\"book_panel_`+ book.id +`\">
              <img class=\"rig-img\" src=\"` + coverURI + `\">
              <span class=\"rig-overlay\"></span>
            </div>
        </li>`);
    }
  }
}

function extendInfoPane(){
  var infoPane = $('#infoPane');
  pageState.infoState = true;
  infoPane.animate({"left":"60vw"}, "slow").addClass('visible');
  resizeRig();
}

function retractInfoPane(){
  var infoPane = $('#infoPane');
  pageState.infoState = false;
  infoPane.animate({"left":"100%"}, "slow").removeClass('visible');
  let infoPhotoRig = $("#infoPhotoRig");
  infoPhotoRig.empty();
  resizeRig();
}

function resizeRig(nanimate){
    let rigID = getActivePageID();
    rigID = rigID.replace('Page', 'Rig')
    var rig = $("#"+rigID)
    var leftMargin = "10vw";
    var rightMargin = "10vw";

    if (pageState.infoState == true){
        rightMargin = "40vw";
        leftMargin = "2vw"
    }
    if (pageState.sideBarState == true){
        leftMargin = "18vw";
    }

    if (nanimate === true){
      rig.css({"margin-left":leftMargin, "margin-right":rightMargin});
    }else{
      rig.animate({"margin-left":leftMargin, "margin-right":rightMargin}, "slow");
    }
}

function GetPanelNumber(path){
  for (let child of path){
      var clickClass = child.className;
      if (clickClass == "rig-cell"){
          var clickID = child.id;
          var panelNum = clickID.split("_").pop();
      }
  }
  return Number(panelNum);
}


function updateCurrentPlayingInfo(currentTitle, currentAuthor, currentChapter){
    $("#currentTitle").text(currentTitle);
    $("#currentAuthor").text("Written by " + currentAuthor);
    $("#currentChapter").text("Chapter " + currentChapter);
}

function toggleArrowDirecion(){
    if (controlButton.hasClass('up')){
        arrowPointDown();
    } else{
        arrowPointUp();
    }
}

function arrowPointUp(){
    var controlButton = $("#playPanelShowControl");
    var contolButtonContainer = $("#playPanelShowControlContainer");
    controlButton.addClass('up');
    contolButtonContainer.animate({'bottom': '0px'}, "slow");
    contolButtonContainer.css({"transform": "rotate(0deg)"});
}

function arrowPointDown(){
    var controlButton = $("#playPanelShowControl");
    var contolButtonContainer = $("#playPanelShowControlContainer");
    controlButton.removeClass('up');
    contolButtonContainer.animate({'bottom': '15vh'}, "slow");
    contolButtonContainer.css({"transform": "rotate(180deg)"});
}

function togglePlayPanel(){
    var playPanel = $("#playPanel");
    if (!playPanel.hasClass('visible')){
        raisePlayPanel();
        return true;
    }else{
        lowerPlayPanel();
        return false;
    }
}

function toggleSideBar(){
    var sideBar = $("#sideBar");
    if (!sideBar.hasClass('visible')){
        extendSideBar();
        return true;
    }
    else{
        retractSideBar();
        return false;
    }
}

function raisePlayPanel(){
    var playPanel = $("#playPanel");
    arrowPointDown();
    playPanel.slideDown("slow");
    playPanel.addClass('visible');

    var infoPane = $("#infoPane")
    infoPane.animate({"height":"75vh"}, "slow");
}

function lowerPlayPanel(){
    var playPanel = $("#playPanel");
    arrowPointUp();
    playPanel.slideUp('slow');
    playPanel.removeClass('visible');

    var infoPane = $("#infoPane")
    infoPane.animate({"height":"90vh"}, "slow");
}

function extendSideBar(){
    var sideBar = $("#sideBar");
    var sideBarToggle = $("#sideBarToggle");
    pageState.sideBarState = true;

    sideBar.animate({"left":"0vw"}, "slow").addClass('visible');
    sideBarToggle.animate({"left":"15vw"}, "slow")
    resizeRig();
}

function retractSideBar(){
    var sideBar = $("#sideBar");
    var sideBarToggle = $("#sideBarToggle");
    pageState.sideBarState = false;

    sideBar.animate({"left":"-15vw"}, "slow").removeClass('visible');
    sideBarToggle.animate({"left":"0"}, "slow")
    resizeRig();
}

function playPanelVisible(){
    return $("#playPanel").hasClass('visible');
}

function smartInfoShow(e, prevPanel, hideOveride, Hide){
  console.log('e is: ', e)
  if (e.path){
    var panelNum = GetPanelNumber(e.path);
  }else{
    var panelNum = GetPanelNumber(e.originalEvent.path);
  }
  console.log("PanelNum is: ", panelNum);
  if (!hideOveride){
      if (panelNum == prevPanel){
        Hide = true;
      }
      else{
        Hide = false;
      }
  }

  toggleinfoPane(panelNum, Hide);
  return {"panelNum": panelNum, "Hide": Hide};
}
