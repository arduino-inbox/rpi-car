var clients = [];
var data_key;

init = function(httpd, key) {
	var io = require('socket.io').listen(httpd);
	io.set('log level', 1);

	data_key = key;

	io.sockets.on('connection', function(socket) {
		clients.push(socket);
		console.log( "Client connected: " + socket );
	});

	io.sockets.on('disconnect', function(socket) {
		clients.pull( clients.indexOf(socket) );
		console.log( "Client disconnected: " + socket );
	});

};

emit = function(data) {
	if ( clients.length > 0 ) {
		console.info("Starting push to clients ...");
		async.eachSeries(
			clients,
			function(socket, callback) {
				socket.emit(data_key, data);
				callback();
			},
			function(err) {
				console.info(err);
			}
		);
	}
};

var static = require('node-static');
var webfolder = new static.Server('.');

processData = function(document) {
	emit(/*data from redis*/);
};

// init HTTP demon
var httpd = require('http').createServer(function(req,res) {
	req.addListener('end', function() {
		webfolder.serve(req,res);
	}
	).resume();
}
);
httpd.listen(8080);

// init client dispatcher
init(httpd, 'measurements_update');

var redis = require("redis"),
        client = redis.createClient(null, 'alarmpi.local');

client.on("error", function (err) {
        console.log("Error " + err);
    });

loop = function () {
  client.lpop('list-acceleration', function (err, data) {
    if (data) {
      console.log("Data:", data);
      //processData({'ACC': data});
    }
    process.nextTick(loop);
  });
};

process.nextTick(loop);