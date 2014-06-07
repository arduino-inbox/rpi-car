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

async = require('async');
emit = function(data) {
	if ( clients.length > 0 ) {
		async.eachSeries(
			clients,
			function(socket, callback) {
				socket.emit(data_key, data);
				callback();
			},
			function(err) {
				//console.info(err);
			}
		);
	}
};

var static = require('node-static');
var webfolder = new static.Server('.');

processData = function(document) {
	emit(document);
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
  client.get('acceleration', function (err, data) {
    if (data) {
      try {
        var value = parseFLoat(data.split('-')[1]) * 1000000;
        processData(value);
        console.log("Value:", value);
      } catch (e) {
        console.log("Error ", e);
      }
    }
    process.nextTick(loop);
  });
};

process.nextTick(loop);