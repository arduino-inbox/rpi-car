var c = null;

var s = require('node-static');
var webfolder = new s.Server('.');

// init HTTP demon
var httpd = require('http').createServer(function (req, res) {
    req.addListener('end', function () {
        webfolder.serve(req, res);
    }).resume();
});
httpd.listen(8080);

// init client dispatcher
var io = require('socket.io').listen(httpd);

io.sockets.on('connection', function (socket) {
    c = socket;
    console.log("Client connected");
});

io.sockets.on('disconnect', function (socket) {
    c = null;
    console.log("Client disconnected");
});

var r = require("redis").createClient(null, 'alarmpi.local');

r.on("error", function (err) {
    console.log("Err:", err);
});

var dataPoints = [
//    'test-gyro-0',
//    'test-gyro-1',
//    'test-gyro-2',
    'test-accel-0',
    'test-accel-1'
//    'test-accel-2'
];

loop = function () {
    dataPoints.forEach(function (p) {
        r.get(p, function (err, data) {
            if (data) {
                c.emit('measurements_update', {
                    key: p,
                    value: data
                });
                //console.log("Value:", data);
            }
            process.nextTick(loop);
        });
    });
};

// run
if (c) process.nextTick(loop);