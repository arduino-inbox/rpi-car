var events = require('events');
var exec = require('child_process').exec;

console.log("killall pi-blaster");
var a1 = exec('killall pi-blaster', function(error, stdout, stderr) {
    console.log('stdout: ', stdout);
    console.log('stderr: ', stderr);
    if (error !== null) {
        console.log('exec error: ', error);
    }

    console.log("pi-blaster");
    var a2 = exec('pi-blaster', function(error, stdout, stderr) {
        console.log('stdout: ', stdout);
        console.log('stderr: ', stderr);
        if (error !== null) {
            console.log('exec error: ', error);
        }
    });
    console.log(a2);


});
console.log(a1);


//a2.on('close', function (code, signal) {
//    console.log("error", "pi-blaster exited with code " + code + " on " + signal + " signal.");
//});
