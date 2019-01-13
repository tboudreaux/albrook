function show(elementID) {
    var ele = document.getElementById(elementID);
    if (!ele) {
        alert("no such element");
        return;
    }
    var pages = document.getElementsByClassName('page');
    for(var i = 0; i < pages.length; i++) {
        pages[i].style.display = 'none';
        pages[i].classList.remove('visible');
    }
    ele.style.display = 'flex';
    ele.classList.add("visible")
    resizeRig(true);
    retractInfoPane();
}

function drawBookGallery(){
  bookRig = $("#bookRig");
  Books = getBooks();
  for (let book of Books['data']){
    coverURI = getCoverURI(book.id, 500, 500);
    bookRig.append(`
      <li>
          <div class=\"rig-cell\" id=\"book_panel_`+ book.id +`\">
            <img class=\"rig-img\" src=\"` + coverURI + `\">
            <span class=\"rig-overlay\"></span>
            <span class=\"rig-text\" id=\"bg_rig-text-` + book.id +`\"><i id=\"playIcon\" class=\"fa fa-play-circle-o\" aria-hidden=\"true\"></i></span>
          </div>
      </li>`);
      let cell = $("#book_panel_"+book.id);
      let cell_text = $("#bg_rig-text-" + book.id);

      cell.click(function(e){
        clickListner(e, "book_panel_", "book");
      });

      cell_text.mousedown(function(){
        updatePlayButtonDown(book.id, "bg_");
      });
      cell_text.mouseup(function(e){
        updatePlayButtonUp(e, book.id, "bg_");
      });
  }
}

function drawAuthorGallery(){
  authorRig = $("#authorRig");
  Authors = getAuthors();
  for (let author of Authors['data']){
    portraitURI = getAuthorPortaitURI(author.id, 500, 500);
    authorRig.append(`
      <li>
          <div class=\"rig-cell\" id=\"author_panel_`+ author.id +`\">
            <img class=\"rig-img\" src=\"` + portraitURI + `\">
            <span class=\"rig-overlay\"></span>
            <span class=\"rig-text\" id=\"ag_rig-text-` + author.id +`\"></span>
          </div>
      </li>`);
      let cell = $("#author_panel_"+author.id);
      cell.click(function(e){
        clickListner(e, "author_panel_", "author");
      });
  }


}
