// main.js
var app = angular.module('myApp', ['ngGrid']);
app.controller('MyCtrl', function($scope) {
    $scope.filterOptions = {
        filterText: ''
    };

    $scope.myData = [{name: "Moroni", age: 50},
                     {name: "Tiancum", age: 43},
                     {name: "Jacob", age: 27},
                     {name: "Nephi", age: 29},
                     {name: "Enos", age: 34}];

    $scope.gridOptions = {
        data: 'myData',
        filterOptions: $scope.filterOptions
    };

    $scope.filterNephi = function() {
        var filterText = 'name:Nephi';
        if ($scope.filterOptions.filterText === '') {
            $scope.filterOptions.filterText = filterText;
        }
        else if ($scope.filterOptions.filterText === filterText) {
            $scope.filterOptions.filterText = '';
        }
    };
});
