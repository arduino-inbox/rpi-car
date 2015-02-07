var events = require('events');
var spawn = require('child_process').spawn;
var pb = spawn('pi-blaster');
pb.stdout.on('data', function (data) {
  console.log('stdout: ' + data);
});

pb.stderr.on('data', function (data) {
  console.log('stderr: ' + data);
});

pb.on('exit', function (code) {
  console.log('child process exited with code ' + code);
});

//exec('killall pi-blaster', function () {
//  var piBlaster = exec('pi-blaster', function (error) {
//    if (error !== null) {
//      console.log('exec error: ', error);
//    }
//  });
//
//  console.log("PID: ", piBlaster.pid);
//  piBlaster.on('close', function (code, signal) {
//    console.log("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
//  });
//
//  piBlaster.stdout.on('data', function(data) {
//    console.log('stdout: ' + data);
//  });
//
//  piBlaster.stderr.on('data', function(data) {
//    console.log('stdout: ' + data);
//  });
//
//});
