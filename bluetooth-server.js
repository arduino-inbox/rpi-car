var btSerial = new (require('bluetooth-serial-port')).BluetoothSerialPort();
	var address = '00-1a-7d-0a-c1-2d';
	var channel = 1;
	
		btSerial.connect(address, channel, function() {
			console.log('connected');
			
			btSerial.on('data', function(buffer) {
				console.log(buffer.toString('utf-8'), Date.now());
			});

		}, function () {
			console.log('cannot connect');
		});

		// close the connection when you're ready
		btSerial.close();

btSerial.inquire();
