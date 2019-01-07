var bookSelector = (function(){
    var currentBook;
    var pub = {};

    pub.ChangeBook = function(newBook){
        currentBook = newBook;
    }

    pub.getBook = function(){
        return currentBook;
    }

    return pub;
}());

var pageState = (function(){
    var infoState;
    var sideBarState;
    var playPanelState;
    var displayingInfo;

    var pub = {};

    pub.ChangeInfoState = function(newState){
        infoState = newState;
    }

    pub.ChangeSideBarState = function(newState){
        sideBarState = newState;
    }

    pub.ChangePlayPanelState = function(newState){
        playPanelState = newState;
    }

    pub.ToggleInfoState = function(){
        infoState = !infoState;
    }

    pub.ToggleSideBarState = function(){
        sideBarState = !sideBarState;
    }

    pub.TogglePlayPanelState = function(){
        playPanelState = !playPanelState;
    }

    return pub;
});