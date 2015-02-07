window.onload = function() {

  var messages = [];
  var socket = io.connect('http://localhost:1337');
  var frm = document.getElementById("frm");
  var field = document.getElementById("field");
  var log = document.getElementById("log");

  socket.on('message', function (data) {
    if(data.message) {
      messages.push(data.message);
      var html = '';
      for(var i=0; i<messages.length; i++) {
        html += messages[i] + '<br />';
      }
      log.innerHTML = html;
    } else {
      console.log("There is a problem:", data);
    }
  });

  frm.onsubmit = function(e) {
    e.preventDefault();
    socket.emit('send', { message: field.value });
    frm.reset();
  };
};