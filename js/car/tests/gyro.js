var mpu6050 = require('mpu6050');

// Instantiate and initialize.
var mpu = new mpu6050();
mpu.initialize();

// Test the connection before using.
mpu.testConnection(function (err, testPassed) {
  if (err) throw new Error(err);
  console.log('testPassed', testPassed);
  if (testPassed) {
    setInterval(function () {
      mpu.getMotion6(function (err, data) {
        console.log(data);
      });
    }, 300);
    // Put the MPU6050 back to sleep.
    //mpu.setSleepEnabled(1);
  }
});
