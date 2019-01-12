$(window).on('load',function(){
  if (getLoggedInStatus() === true){
    // Queue of things to do when authenticated
    drawBookGallery();
    addBookClickListner();
    playPanelSetup();
    sideBarSetup();
    authorInfoSetup();
    audioSetup();
    drawAuthorGallery();
    addAuthorClickListner()
  }
  else{
    logIn();
  }

});


function logIn(){
  $('#ex1').modal('show');
}
