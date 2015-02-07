var events = require('events');
var exec = require('child_process').exec;

exec('killall pi-blaster', function () {
  var piBlaster = exec('pi-blaster', function (error) {
    if (error !== null) {
      console.log('exec error: ', error);
    }
  });

  console.log("PID: ", piBlaster.pid);
  piBlaster.on('close', function (code, signal) {
    console.log("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
  });
  piBlaster.stdout.pipe(console.log);
  piBlaster.stderr.pipe(console.log);
});
