"use strict";


function replaceStar(result){
    $('#message').html("Star Added!");
}

function addStar(evt) {
    evt.preventDefault();

    var url = "/add_to_saved/" + $('#addStar').val();
    $.get(url, replaceStar);
}

$('#addStar').on('click', addStar);

document.getElementById("directionValues").selectedIndex = -1;

//from jquery geocomplete plug in 
$(function(){
        $("#geocomplete").geocomplete({
          details: "form",
          types: ["geocode", "establishment"],
        });
      });