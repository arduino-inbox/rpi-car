var events = require('events');
var child = require('child_process');

console.log("child.spawn('pi-blaster')");
piBlasterProc = child.spawn(
    'pi-blaster',
    {
        stdio: [0, 'pipe', 'pipe']
    }
);
console.log('Spawned child pid: ' + piBlasterProc.pid);

piBlasterProc.on('close', function (code, signal) {
    console.log("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
});
