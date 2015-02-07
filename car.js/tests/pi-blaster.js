var events = require('events');
var spawn = require('child_process').spawn;
var pb = spawn('pi-blaster', function (code, stdout, stderr) {
  console.log('child process exited with code ' + code);
  console.log(stdout, stderr);
});
console.log("pid:", pb.pid);

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
