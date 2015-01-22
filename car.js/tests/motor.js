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
  if (speed > 1) speed = 1; // fix

  if (speed < 1) {
    setTimeout(increaseSpeed, 300);
  } else {
    setTimeout(decreaseSpeed, 300);
  }
};

decreaseSpeed = function () {
  piblaster.setPwm(pwmPin, speed);
  speed -= 0.1;
  if (speed < 0) speed = 0; // fix

  if (speed > 0) {
    setTimeout(decreaseSpeed, 300);
  }
};

increaseSpeed();


