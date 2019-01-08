function getSecondsFromTimestring(timestring){
    var splitTime = timestring.split(':');
    var seconds = (+splitTime[0]) * 60 * 60 + (+splitTime[1]) * 60 + (+splitTime[2]); 
    return seconds;
}

function mouseUp(e)
{
    // var offsetX = $(this).offset().left
    // var posX = e.pageX - offsetX
    // var totalWidth = $("#progress").width();
    // updateTrackPosition(posX/totalWidth);

    window.removeEventListener('mousemove', handelMove, true);
}

function mouseDown(e)
{
    window.addEventListener('mousemove', handelMove, true);
}

function fmtMSS(s){return(s-(s%=60))/60+(9<s?':':':0')+s}