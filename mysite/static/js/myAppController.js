// Instantiate the Angular app
var myApp = angular.module('myApp', ['ngRoute']);

// Factory to return data from RESTful api
myApp.factory('dataFactory', function($http) {

    // modified from: http://weblogs.asp.net/dwahlin/using-an-angularjs-factory-to-interact-with-a-restful-service
     
    // url to query
    var urlBase = '/threads';
    var dataFactory = {};

    // get all forum threads from the api (query /threads URL)
    dataFactory.getThreads = function () {
        return $http.get(urlBase)
    };

    // get a particular forum thread from api
    dataFactory.getOneThread = function (thread_id) {
        return $http.get(urlBase + '/' + thread_id)
    };

    // get comments for a particular forum thread from api
    dataFactory.getOneThreadComments = function (thread_id) {
        return $http.get(urlBase + '/' + thread_id + '/comments/')
    };

    return dataFactory;
 
});

// Controller for listing threads and submitting threads via form
myApp.controller('threadController', function($scope, $http, dataFactory) {

    // function to get thread list via a call to the factory function
    $scope.getThreadlist = function() {
        dataFactory.getThreads()
            .success(function (response) {
                $scope.myThreads = response;
            })
            .error(function (error) {
                $scope.status = 'Unable to load data: ' + error.message;
            });	
    };

    // call it!
    $scope.getThreadlist();

    // This function will submit the user-provided data in the Create Thread form
    // to the URL /create_post/, at which point the Django view will take over 
    // to add this information into the database
    // modified from http://django-angular.readthedocs.org/en/latest/angular-model-form.html
    $scope.submit = function() {

	// console.log($scope.userthread)

	// POST $scope.userthread JSON to create_post/ URL
        $http.post('create_post/', $scope.userthread)
	    .success(function(out_data) {
		// re-list the threads, since updates have happened
                $scope.getThreadlist();
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = {
                    "data": data,
                    "status": status,
                    "headers": header,
                    "config": config 
                }
	        // console.log($scope.ResponseDetails)
            });
	    
	// clear the form
        $scope.userthread = {}
    };

});

// Controller for comments view
myApp.controller('commentController', function($scope, $http, $routeParams, dataFactory) {

    // grab variable part of URL (i.e., the thread id)
    var currentId = $routeParams.threadid;

    // starting to violate DRY - fix later!
    // function to get comments via a call to the factory function
    $scope.getCommentlist = function() {
	dataFactory.getOneThreadComments(currentId)
            .success(function (response) {
                $scope.myComments = response;
            })
            .error(function (error) {
                $scope.status = 'Unable to load data: ' + error.message;
            });	
    };

    // DRY violations - fix later!
    // function to get associated thread via a call to the factory function
    $scope.getSpecificThread = function() {
	dataFactory.getOneThread(currentId)
            .success(function (response) {
                $scope.myCommentThread = response;
            })
            .error(function (error) {
                $scope.status = 'Unable to load data: ' + error.message;
            });	
    };

    // call these functions
    $scope.getCommentlist();
    $scope.getSpecificThread();

    // DRY violations - fix later!
    $scope.submit = function() {

	// set thread id of comment
	$scope.usercomment.mythreadid = currentId
	
	// console.log($scope.usercomment)

	// POST $scope.usercomment JSON to create_comment/ URL
        $http.post('create_comment/', $scope.usercomment)
	    .success(function(out_data) {
		// re-list the comments, since updates have happened
                $scope.getCommentlist();
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = {
                    "data": data,
                    "status": status,
                    "headers": header,
                    "config": config 
                }
	        // console.log($scope.ResponseDetails)
            });
	    
	// clear the form
        $scope.usercomment = {}
    };

    $scope.likeComment = function(commentId) {

	// initialize variable
        $scope.usercomment = {}

	// set comment id of comment
	$scope.usercomment.mycommentid = commentId
	
	// console.log($scope.usercomment)

	// POST $scope.usercomment JSON to like_comment/ URL
        $http.post('like_comment/', $scope.usercomment)
	    .success(function(out_data) {
		// re-list the comments, since updates have happened
                $scope.getCommentlist();
            })
            .error(function (data, status, header, config) {
                $scope.ResponseDetails = {
                    "data": data,
                    "status": status,
                    "headers": header,
                    "config": config 
                }
	        // console.log($scope.ResponseDetails)
            });
    };

});

// Angular routing to partials
myApp.config(function ($routeProvider, $locationProvider) {

    // Saying '/' actually means: http://myurl.com/#/
    // Saying '/test' actually means: http://myurl.com/#/test and so on
    // In this awkward way, conflicts between Django's URL routing mechanism and
    // Angular's are avoided, since Django only deals with non-# paths

    // switch between the thread view (default) and the comment view
    $routeProvider
        .when('/', {
            templateUrl: '/static/partials/threadview.html',
            controller: 'threadController'
        })
        .when('/comments/:threadid', {
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
