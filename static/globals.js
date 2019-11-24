$(document).ready(function() {
    $('#left-btn').on('click',{dir: "left"}, sendAngle);
    $('#right-btn').on('click',{dir: "right"}, sendAngle);
    $('#up-btn').on('click',{dir: "up"}, sendAngle);
    $('#down-btn').on('click',{dir: "down"}, sendAngle);
});
// $(document).keypress(function(e) {
//     if(e.which == 13 || e.keyCode == 13) {
//         sendAngle();
//     }
// });
function sendAngle(event) {
    var direction = event.data.dir
    var send = {
        payload: direction
    };
    console.log(send);
    $.ajax({
        type:'POST',
        data:JSON.stringify(send),
        url:'/horizontal',
        dataType:'JSON'
    }).done(function(response) {
        console.log(response.data.data.horz);
        $('#current-pos').text(response.data.data.horz);
    });
}
