var events = require('events');
var child = require('child_process');

console.log("child.spawn('pi-blaster')");
piBlasterProc = child.spawn('pi-blaster');

piBlasterProc.stdout.on('data', function (data) {
    console.log("pi-blaster::stdout: " + data);
});

piBlasterProc.stderr.on('data', function (data) {
    console.log("pi-blaster::stderr: " + data);
});

piBlasterProc.on('close', function (code, signal) {
    console.log("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
});
