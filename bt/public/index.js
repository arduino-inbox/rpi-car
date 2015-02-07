$(function() {
  var $frm = $("#frm");
  var $field = $("#field");
  var socket = io.connect('http://localhost:1337');

  socket.on('runtime', function (runtime) {
    $('.runtime').html(runtime);
  });

  socket.on('message', function (message) {
    if (message.error) {
     $('<div class="alert alert-danger alert-dismissible" role="alert">' +
     '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
     '<span aria-hidden="true">&times;</span>' +
     '</button>' +
     message.error +
     '</div>').appendTo("body");
    } else if (message.info) {
      $('<div class="alert alert-info alert-dismissible" role="alert">' +
      '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
      '<span aria-hidden="true">&times;</span>' +
      '</button>' +
      message.error +
      '</div>').appendTo("body");
    } else if (message.input) {
      var $sensor = $('#' + message.input.sensor);
      if (!$sensor.length) {
        $('<div id="'+message.input.sensor+'">' +
        '<h2>' +
          message.input.sensor +
        '</h2>' +
        '<h3>' +
          message.input.parameter +
          ': <span class="value">' +
          message.input.value +
          '</span>' +
        '</h3>' +
        '</div>').appendTo("#dashboard");
      } else {
        $sensor.find('.value').html(message.input.value);
        $sensor.find('.time').html(message.input.time);
      }
    } else {
      console.log(message);
    }
  });

  $frm.submit(function (event) {
    event.preventDefault();
    socket.emit('send', $field.val());
    $frm[0].reset();
  });
});