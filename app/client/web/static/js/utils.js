function getSecondsFromTimestring(timestring){
    var splitTime = timestring.split(':');
    var seconds = (+splitTime[0]) * 60 * 60 + (+splitTime[1]) * 60 + (+splitTime[2]);
    return seconds;
}

function mouseUp(e)
{

    window.removeEventListener('mousemove', handelMove, true);
}

function mouseDown(e)
{
    window.addEventListener('mousemove', handelMove, true);
}

function fmtMSS(s){return(s-(s%=60))/60+(9<s?':':':0')+s}

String.prototype.toHHMMSS = function () {
    var sec_num = parseInt(this, 10);
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}

    if (hours == 0){
        return minutes+':'+seconds;
    }
    else{
        if (hours < 10) {hours = "0"+hours;}
        return hours+':'+minutes+':'+seconds;
    }
}

function getActivePageID(){
  var pages = document.getElementsByClassName('page');
  for(var i = 0; i < pages.length; i++) {
      if (pages[i].classList.contains('visible')){
          return pages[i].id
      }
  }
}
