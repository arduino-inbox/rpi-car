var clients = [];
var data_key;

init = function(httpd, key) {
	var io = require('socket.io').listen(httpd);

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
        console.log("Err:", err);
    });

var dataPoints = [
    'test-gyro-0',
    'test-gyro-1',
    'test-gyro-2',
    'test-accel-0',
    'test-accel-1',
    'test-accel-2'
];

loop = function () {
//  client.get('acceleration', function (err, data) {
//    if (data) {
//      try {
//        var value = parseFloat(data);
//        processData(value);
//        //console.log("Value:", value);
//      } catch (e) {
//        //console.log("Error ", e);
//      }
//    }
//    process.nextTick(loop);
//  });

  dataPoints.forEach(function (p) {
      client.get(p, function (err, data) {
        if (err) {
            console.log("Err:", err);
        }
        else if (data) {
          try {
            processData({
                key: p,
                value: data
            });
            //console.log("Value:", data);
          } catch (e) {
            console.log("Err:", e);
          }
        }
        process.nextTick(loop);
      });
  });
};

process.nextTick(loop);