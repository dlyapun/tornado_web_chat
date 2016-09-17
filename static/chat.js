var ws = new WebSocket("wss://127.0.0.1:5000/ws");

ws.onmessage = function (evt) {
    var data = JSON.parse(evt.data)
    var name = data['name']
    var msg = data['msg']
    var date = data['date']
    $('.table > tbody:last').append(
        '<tr><td class="col-md-4"><b>' + name +
        ':</b></td><td class="col-md-8">' + msg +'</td><td class="col-md-8">' + date +'</td></tr>'
    );
    var n = $(document).height();
    $('html, body').animate({ scrollTop: n });
};

$('#msg_form').submit(function(){
    $message = $("input[name='msg']")
    room = window.location.href.split('/')[4];
    var msg = $message.val()
    if (msg.length < 4) {
        $("#message_form_id").addClass( "has-error" );
    }
    else{
        $message.val('');

        var msg = {
          msg: msg,
          room: room
        };

        var str = JSON.stringify(msg);
        console.log(str)
        ws.send(str);
        return false;
    }
});
