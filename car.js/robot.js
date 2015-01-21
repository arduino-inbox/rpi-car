var Robot = function (config) {
  var self = this;
  self.config = config;
  self.nodes = [];

  console.log("Configuring nodes");
  self.config.nodes.forEach(function (node) {
    console.log("-", node.name);
    var nodeClass = require('./nodes/' + node.name);
    var nodeInstance = new nodeClass(node.config);
    self.nodes.push({
      name: node.name,
      instance: nodeInstance
    });
  });

  return {
    work: function () {
      console.log("Starting nodes");
      self.nodes.forEach(function (node) {
        console.log("-", node.name);
        node.instance.on('update', function (param, value) {
          console.log("[", (new Date()).getTime(), "] ", "update", node.name, "", param, "", value);
        });
        node.instance.work();
      });
    }
  }
};

var robot = new Robot({
  nodes: [
    {
      name: "ultrasonic",
      config: {
        echoPin: 22,
        triggerPin: 24,
        timeout: 500, // smaller values always return -1
        interval: 50 // @todo to fiddle with
      }
    }
  ]
});

robot.work();