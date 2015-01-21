var ultrasonic = new (require('./nodes/ultrasonic'))();
//setTimeout(function () {
  var distance = ultrasonic.getDistance();
  console.log('distance:', distance);
//}, 30); // warm up timeout