var piblaster = require('pi-blaster.js');
var onoff = require('onoff');

var speed = 0;
var d1 = new onoff.Gpio(17, 'out');
var d2 = new onoff.Gpio(27, 'out');
var pwmPin = 25;
var incr = 1;

var p1 = 1;
var p2 = 0;

if (process.argv[2] == "back") {
  p1 = 0;
  p2 = 1;
}

// forward
d1.writeSync(p1);
d2.writeSync(p2);

increaseSpeed = function () {
  piblaster.setPwm(pwmPin, speed);
  speed += 0.1;
  if (speed > 0.5) speed = 0.5; // fix

  if (speed < 0.5) {
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


