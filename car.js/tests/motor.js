var piblaster = require('pi-blaster.js');
var onoff = require('onoff');

var speed = 0;
var d1 = new onoff.Gpio(17, 'out');
var d2 = new onoff.Gpio(27, 'out');
var pwmPin = 25;
var incr = 1;

// forward
d1.writeSync(1);
d2.writeSync(0);

increaseSpeed = function () {
  piblaster.setPwm(pwmPin, speed);
  speed += 0.1;
  if (speed < 1) {
    setTimeout(increaseSpeed, 10);
  } else {
    setTimeout(decreaseSpeed, 10);
  }
};

decreaseSpeed = function () {
  piblaster.setPwm(pwmPin, speed);
  speed -= 0.1;
  if (speed > 0) {
    setTimeout(decreaseSpeed, 10);
  }
};

increaseSpeed();


