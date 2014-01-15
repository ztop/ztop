angular.module('clientApp', [])
  .factory('Data', function($timeout) {
    var sock = new ReconnectingWebSocket('ws://localhost:9000');

    var listeners = [];

    sock.onmessage = function(e) {
      var data = JSON.parse(e.data);
      listeners.forEach(function(fn) {
        $timeout(function() { fn(data); }, 0);
      });
    };

    return {
      register: function(fn) {
        listeners.push(fn);
      },

      unregister: function(fn) {
        var index = listeners.indexOf(fn);
        if (index > -1) {
            listeners.splice(index, 1);
        }
      }
    }
  })
  .controller('MainCtrl', function($scope, Data) {
    Data.register(function(data) {
      $scope.processes = data;
    });

    $scope.hasCpuPercent = function(p) { return typeof p.cpu_percent === 'number'; }
  });