function getSyncStream(book_id, chapter_id){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+book_id+"/chapter:"+chapter_id+"/stream", false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function getCurrentTrackInfo (book_id, user_id){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+book_id+"/uid:"+user_id+"/currentTrack", false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function getAuthorInfo(author_name){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Author/name:"+author_name, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function getCoverURI(indexNum, width, height){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Book/id:"+indexNum+"/cover/width:"+width+"/height:"+height , false );
    xmlHttp.send( null );
    return xmlHttp.responseText; 
}

function getAuthorPortaitURI(authorID, width, height){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/Author/id:"+authorID+"/portrait/width:"+width+"/height:"+height , false );
    xmlHttp.send( null );
    return xmlHttp.responseText; 
}