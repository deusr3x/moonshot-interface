$(document).ready(function() {
    $('#send-btn').on('click', sendAngle);
});
$(document).keypress(function(e) {
    if(e.which == 13 || e.keyCode == 13) {
        sendAngle();
    }
});

function sendAngle() {
    var degrees = $('#degrees').val();
    var send = {
        payload: degrees
    };

    $.ajax({
        type:'POST',
        data:JSON.stringify(send),
        url:'/degrees',
        dataType:'JSON'
    }).done(function(response) {
        console.log(response);
    });
}