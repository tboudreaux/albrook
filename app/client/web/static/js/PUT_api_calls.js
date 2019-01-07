function putAudioPosition(user_id, book_id){
    var xmlHttp = new XMLHttpRequest();
    var mimeType = "application/json";  
    xmlHttp.open('PUT', "/Book/id:" + book_id + "/uid:" + user_id + "/currentTrack", true);  // true : asynchrone false: synchrone
    xmlHttp.setRequestHeader('Content-Type', mimeType);  
    xmlHttp.send(JSON.stringify({name:"John Rambo", time:"2pm"})); 
}