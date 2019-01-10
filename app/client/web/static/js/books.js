function toggleinfoPane(info, panelNum, Hide) {
    var indexNum = panelNum - 1;
    $("#infoTitle").text(info.titles[indexNum]);
    $("#infoAuthor").text(info.authors[indexNum]);
    $("#infoNarrator").text(info.narrators[indexNum]);
    $("#infoDesc").text(info.descs[indexNum]);

    var coverURI = getCoverURI(panelNum, 300, 300);
    document.getElementById('infoPhoto').src = coverURI;

    bookSelector.ChangeBook(indexNum);
    {
        var infoPane = $('#infoPane');
        if (!infoPane.hasClass('visible')){
            pageState.infoState = true;
            infoPane.animate({"left":"60vw"}, "slow").addClass('visible');
            resizeBookRig();
        }
        else {
            if (Hide === true){
                pageState.infoState = false;
                infoPane.animate({"left":"100%"}, "slow").removeClass('visible');
                resizeBookRig();
            }
        }
    };
}

function resizeBookRig(){
    var rig = $("#rig")
    var leftMargin = "10vw";
    var rightMargin = "10vw";

    if (pageState.infoState == true){
        rightMargin = "40vw";
        leftMargin = "2vw"
    }
    if (pageState.sideBarState == true){
        leftMargin = "18vw";
    }

    rig.animate({"margin-left":leftMargin, "margin-right":rightMargin}, "slow");
}

function GetPanelNumber(path){
    for (let child of path){
        var clickClass = child.className;
        if (clickClass == "rig-cell"){
            var clickID = child.id;
            var panelNum = clickID.split("_")[2];
        }
    }
    return panelNum;
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
    resizeBookRig()
}

function retractSideBar(){
    var sideBar = $("#sideBar");
    var sideBarToggle = $("#sideBarToggle");
    pageState.sideBarState = false;

    sideBar.animate({"left":"-15vw"}, "slow").removeClass('visible');
    sideBarToggle.animate({"left":"0"}, "slow")
    resizeBookRig()
}

function playPanelVisible(){
    return $("#playPanel").hasClass('visible');
}

function smartInfoShow(e, prevPanel, hideOveride, Hide){
    var panelNum = GetPanelNumber(e.path);
    if (!hideOveride){
        if (panelNum == prevPanel){
          Hide = true;
        }
        else{
          Hide = false;
        }
    }

    toggleinfoPane(info, panelNum, Hide);
    return {"panelNum": panelNum, "Hide": Hide};
}

function showAuthorInfo(authorName){
    authorInfo = getAuthorInfo(authorName);
    authorName = authorInfo['data'][0].firstName + " " + authorInfo['data'][0].lastName;
    if (authorInfo['data'][0].middleName !== null){
        authorName = authorName.replace(' ', " " + authorInfo['data'][0].middleName + " ") ;
    }

    $("#infoTitle").text(authorName);
    $("#infoAuthor").text(authorInfo['data'][0].nationality);
    $("#infoNarrator").text("");
    $("#infoDesc").text(authorInfo['data'][0].biography);

    var portraitURI = getAuthorPortaitURI(authorInfo['data'][0]['id'], 300, 300);
    document.getElementById('infoPhoto').src = portraitURI;
}
