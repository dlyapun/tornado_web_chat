// Support TLS-specific URLs, when appropriate.
if (window.location.protocol == "https:") {
  var ws_scheme = "wss://";
} else {
  var ws_scheme = "ws://"
};

var ws = new WebSocket(ws_scheme + location.host + "/ws");

// var ws = new WebSocket("wss://127.0.0.1:5000/ws");

ws.onmessage = function (evt) {
    var data = JSON.parse(evt.data)
    var name = data['name']
    var msg = data['msg']
    var date = data['date']
    // $('.table > tbody:last').append(
    //     '<tr><td class="col-md-4"><b>' + name +
    //     ':</b></td><td class="col-md-8">' + msg +'</td><td class="col-md-8">' + date +'</td></tr>'
    // );
    $('#message_media_id').append(
        '<li class="media message_media"> <div class="media-body"> <div class="media"> <div class="media-body"> <small class="text-muted"><strong>'+ name +'</strong> | '+date+'</small><br /> '+ msg +' </div> </div> </div> </li>'
    );
    var n = $(document).height();
    $('html, body').animate({ scrollTop: n });
};

ws.onclose = function(event) {
  if (event.wasClean) {
    console.log('Соединение закрыто чисто');
  } else {
    console.log('Обрыв соединения'); // например, "убит" процесс сервера
  }
  console.log('Код: ' + event.code + ' причина: ' + event.reason);
};

ws.onerror = function(error) {
  console.log("Ошибка " + error.message);
};

ws.onopen = function() {
  console.log("Соединение установлено.");
};


$('#msg_form').submit(function(){
    $message = $("input[name='msg']")
    room = window.location.pathname.split('/')[2];
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
