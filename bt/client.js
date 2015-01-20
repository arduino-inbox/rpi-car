#!/usr/bin/env node

var btSerial = new (require('bluetooth-serial-port')).BluetoothSerialPort();
var address = '70:73:CB:C3:66:98';
var channel = 3;
var message = 'ping\r\n';

btSerial.connect(address, channel, function () {
    console.log('connected:', address, channel);

    btSerial.on('data', function (data) {
        console.log('[' + (new Date()).getTime() + ']', 'received:', data.toString());
    });

    setInterval(function () {
        btSerial.write(new Buffer(message, 'utf-8'), function (err) {
            console.log('[' + (new Date()).getTime() + ']', 'sent:', message);
            if (err) {
                console.log(err);
            }
        });
    }, 1000);

}, function () {
    console.log('cannot connect');
});

// close the connection when you're ready
//btSerial.close();
btSerial.inquire();