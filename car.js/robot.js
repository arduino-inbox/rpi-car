var ultrasonic = new (require('./nodes/ultrasonic'))();
var distance = ultrasonic.getDistance();
console.log('distance:', distance);