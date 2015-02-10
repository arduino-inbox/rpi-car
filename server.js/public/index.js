$(function() {
  var $frm = $("#frm");
  var $field = $("#field");
  var socket = io.connect('http://localhost:1337');

  socket.on('runtime', function (runtime) {
    $('.runtime').html(runtime);
    $('title').html('Car: '+runtime);
  });

  socket.on('message', function (message) {
    if (message.error || message.info) {
     $('<div class="alert ' + (message.error ? 'alert-danger' : 'alert-info') + ' alert-dismissible" role="alert">' +
     '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
     '<span aria-hidden="true">&times;</span>' +
     '</button>' +
     (message.error || message.info) +
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
        '<h4 class="aux-head hidden">' +
          'aux: <span class="aux">' +
          message.input.aux +
          '</span>' +
        '</h4>' +
        '</div>').appendTo("#dashboard");
      } else {
        $sensor.find('.value').html(message.input.value);
        if (message.input.aux) {
          $sensor.find('.aux').html(message.input.aux);
          $sensor.find('.aux-head').removeClass('hidden');
        } else {
          $sensor.find('.aux-head').addClass('hidden');
        }
      }
    } else {
      console.log(message);
    }
  });

  $frm.submit(function (event) {
    event.preventDefault();
    socket.emit('send', $field.val());
  });

  $('.run').click(function () {
    $field.val('run');
    $frm.submit();
  });
  $('.fwd').click(function () {
    $field.val('goForward:'+$('.speed').val());
    $frm.submit();
  });
  $('.bwd').click(function () {
    $field.val('goBackward:'+$('.speed').val());
    $frm.submit();
  });
  $('.stop').click(function () {
    $field.val('stop');
    $frm.submit();
  });
});