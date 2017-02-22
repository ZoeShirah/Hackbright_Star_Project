"use strict";


function replaceStar(result){
    $('#message').html(result);
}

function addStar(evt) {
    evt.preventDefault();

    var url = "/add_to_saved/" + $('#addStar').val();
    $.get(url, replaceStar);
}

$('#addStar').on('click', addStar);

