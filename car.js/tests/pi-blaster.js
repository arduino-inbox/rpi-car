var events = require('events');
var exec = require('child_process').exec;

exec('killall pi-blaster', function (error, stdout, stderr) {
  if (error !== null) {
    console.log('exec error: ', error);
  }

  console.log("pi-blaster");
  var piBlaster = exec('pi-blaster', function (error, stdout, stderr) {
    console.log('stdout: ', stdout);
    console.log('stderr: ', stderr);
    if (error !== null) {
      console.log('exec error: ', error);
    }
  });
  console.log("PID: ", piBlaster.pid);
  piBlaster.on('close', function (code, signal) {
      console.log("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
  });
});
