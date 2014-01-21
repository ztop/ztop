angular.module('clientApp', [])
  .factory('Data', function($rootScope) {
    var sock = new ReconnectingWebSocket('ws://localhost:9000');
    var data = [];

    sock.onmessage = function(e) {
      $rootScope.$apply(function() {
        data.length = 0;
        JSON.parse(e.data).forEach(function(d) { data.push(d); });
      });
    };

    return data;
  })
  .controller('MainCtrl', function($scope, Data) {
    $scope.processes = Data;

    $scope.hasCpuPercent = function(p) { return typeof p.cpu_percent === 'number'; };
  });