var events = require('events');

function Robot(config) {
  var self = this;
  self.config = config;
  self.nodes = [];
  self.started = (new Date()).getTime();

  var uptime = function () {
    return (((new Date()).getTime() - self.started) / 1000).toFixed(4);
  };

  console.log("Configuring nodes");
  self.config.nodes.forEach(function (node) {
    console.log("-", node.name);
    var nodeClass = require('./nodes/' + node.name);
    var nodeInstance = new nodeClass(self, node.config);
    self.nodes.push({
      name: node.name,
      instance: nodeInstance
    });
  });

  self.work = function () {
    console.log("Starting nodes");
    self.nodes.forEach(function (node) {
      console.log("-", node.name);
      node.instance.on('update', function (param, value) {
        self.emit('nodeUpdate', self.uptime(), node.name, param, value);
        console.log("[", uptime(), "]", "update", node.name, "", param, "", value);
      });
      node.instance.on('info', function (message) {
        console.log("[", uptime(), "]", "info", node.name, "", message);
      });
      node.instance.work();
    });
  }
}
Robot.prototype.__proto__ = events.EventEmitter.prototype;


// Run
var robot = new Robot({
  nodes: [
    {
      name: "ultrasonic",
      config: {
        echoPin: 22,
        triggerPin: 24,
        timeout: 1000, // values smaller than 500 always return -1
        interval: 50 // @todo to fiddle with
      }
    },
    {
      name: "transmitter",
      config: {
        address: '70:73:CB:C3:66:98',
        channel: 3
      }
    }
  ]
});
robot.work();