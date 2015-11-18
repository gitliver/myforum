var myApp = angular.module('myApp', []);

myApp.controller('myController', function($scope, $http) {
    $http.get("/threads").success(function(response) {$scope.myThreads = response;});
});
