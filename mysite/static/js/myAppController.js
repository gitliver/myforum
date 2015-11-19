// Instantiate the Angular app
var myApp = angular.module('myApp', ['ngResource', 'ngRoute']);

// Controller for listing threads and submitting threads via form
myApp.controller('threadController', function($scope, $http) {

    // function to get JSON data for the forum threads via the /threads URL
    $scope.list = function() {
        $http.get("/threads").success(function(response) {$scope.myThreads = response;});
    };

    // call it!
    $scope.list();

    // This function will submit the user-provided data in the Create Thread form
    // to the URL /create_post/, at which point the Django view will take over 
    // to add this information into the database
    // modified from http://django-angular.readthedocs.org/en/latest/angular-model-form.html
    $scope.submit = function() {

	console.log($scope.user)

	// POST $scope.user JSON to create_post/ URL
        $http.post('create_post/', $scope.user)
	    .success(function(out_data) {
		// re-list the threads, since updates have happened
                $scope.list();
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = {
                    "data": data,
                    "status": status,
                    "headers": header,
                    "config": config 
                }
	        console.log($scope.ResponseDetails)
            });
	    
	// clear the form
        $scope.reset = function() {
           $scope.user = {}
        };    

        $scope.reset();
    };

});

// Controller for comments view
myApp.controller('commentController', function($scope, $http) {
    console.log("Testing ...")
});

// Angular routing to partials
myApp.config(function ($routeProvider, $locationProvider) {

    // Saying '/' actually means: http://myurl.com/#/
    // Saying '/test' actually means: http://myurl.com/#/test and so on
    // In this awkward way, conflicts between Django's URL routing mechanism and
    // Angular's are avoided, since Django only deals with non-# paths

    $routeProvider
        .when('/', {
            templateUrl: '/static/partials/threadview.html',
            controller: 'threadController'
        })
        .when('/comments', {
            templateUrl: '/static/partials/commentview.html',
            controller: 'commentController'
        })
        .when('/comments/:id', {
            templateUrl: '/static/partials/commentview.html',
            controller: 'commentController'
        })
        .otherwise({
            redirectTo: '/'
            // templateUrl: '/static/partials/threadview.html'
        });

    // $locationProvider.html5Mode(true);

});

// Add stuff to header, deal with csrftoken issue
// modified from http://django-angular.readthedocs.org/en/latest/integration.html (see the discussion there)
myApp.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
