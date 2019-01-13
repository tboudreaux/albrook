function getSyncStream(book_id, chapter_id){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+book_id+"/chapter:"+chapter_id+"/stream", false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
  }else{
    logIn();
  }
}

function getCurrentTrackInfo (book_id){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+book_id+"/currentTrack", false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getBookInfo(book_id){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+book_id, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getNumBooks(){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Books/number", false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getBooks(){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Books", false);
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getAuthors(){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Authors", false);
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getBooksByAuthorByBook(book_id){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Books/author/"+book_id, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    login()
  }
}


function getAuthorInfoName(author_name){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Author/name:"+author_name, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getAuthorInfo(author_id){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Author/"+author_id, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}

function getAuthorBooks(author_id){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Author/"+author_id+"/books", false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
  }else{
    logIn();
  }
}


function getCoverURI(indexNum, width, height){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+indexNum+"/cover/width:"+width+"/height:"+height , false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
  }else{
    logIn();
  }
}

function getAuthorPortaitURI(authorID, width, height){
  if (getLoggedInStatus() === true){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Author/id:"+authorID+"/portrait/width:"+width+"/height:"+height , false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
  }else{
    logIn();
  }
}

function getLoggedInStatus(){
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", "/User/loggedin", false );
  xmlHttp.send( null );
  let loggedInStatus = xmlHttp.responseText;
  return loggedInStatus == "True";
}
