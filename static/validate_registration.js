$('.user-info').on('submit', function(evt) {

    var userChars = $('#e-mail').val();
    var passChars = $('#password').val().length;

    if ((/(.+)@(.+\.){1,}(com|net|gov|edu)/g).test(userChars) === false) {
        evt.preventDefault();
        alert('please enter a valid email');
    } else if (passChars < 3) {
        evt.preventDefault();
        alert('password must be at least 3 characters');
    }

});
