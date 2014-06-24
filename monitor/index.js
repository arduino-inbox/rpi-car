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
var r = require("redis").createClient(null, 'alarmpi.local');

r.on("error", function (err) {
    console.log("Err:", err);
});

var dataPoints = [
    'accel-x',
    'accel-y'
];

loop = function () {
    dataPoints.forEach(function (p) {
        r.get(p, function (err, data) {
           if (data) {
                c.emit('measurements_update', {
                    key: p,
                    value: data
                });
            }
            process.nextTick(loop);
        });
    });
};

io.sockets.on('connection', function (socket) {
    c = socket;
    console.log("Client connected");
    // run
    process.nextTick(loop);
});

io.sockets.on('disconnect', function (socket) {
    c = null;
    console.log("Client disconnected");
    process.exit();
});

