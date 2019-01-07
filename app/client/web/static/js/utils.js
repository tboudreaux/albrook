function getSecondsFromTimestring(timestring){
    var splitTime = timestring.split(':');
    var seconds = (+splitTime[0]) * 60 * 60 + (+splitTime[1]) * 60 + (+splitTime[2]); 
    return seconds;
}