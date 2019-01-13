function updatePlayButtonDown(panelNum, idPref){
  pageState.displayingInfo = 'book';
  $("#" + idPref + "rig-text-"+panelNum).html("<i class=\"fa fa-play-circle\"></i>");
}

function updatePlayButtonUp(e, panelNum, idPref){
  pageState.displayingInfo = 'book'
  $("#" + idPref + "rig-text-"+panelNum).html("<i class=\"fa fa-play-circle-o\"></i>");
  smartInfo = smartInfoShow(e, prevPanel, true, false);
  prevPanel = smartInfo.panelNum;
  Hide = smartInfo.Hide;

  playClick(panelNum);
}

function clickListner(e, idPref, state){
  pageState.displayingInfo = state;
  if (e.target === this){
    smartInfo = smartInfoShow(e, prevPanel, true, false);
  }else{
    smartInfo = smartInfoShow(e, prevPanel, false, Hide);
  }
  prevPanel = smartInfo.panelNum;
  Hide = smartInfo.Hide;
}
