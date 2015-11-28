// Instantiate the Angular app
var myApp = angular.module('myApp', ['ngRoute', 'ngCookies']);

// Factory to return data from or post data to RESTful api
myApp.factory('dataFactory', function($http) {

    var dataFactory = {};

    // reading:
    // http://chariotsolutions.com/blog/post/angularjs-corner-using-promises-q-handle-asynchronous-calls/
    // http://www.codelord.net/2015/05/25/dont-use-$https-success/
    // Note: "The $http legacy promise methods success and error have been deprecated.
    // Use the standard then method instead." ---docs

    // http GET call to retrieve api data (forum thread, all forum threads, or forum thread's comments)
    dataFactory.getApiData = function (myUrl) {
        return $http.get(myUrl)
            .then(function(response) {
                return response.data;
            },
            function (httpError) {
                throw httpError.status + " : " + httpError.data;
            });
    };

    // http POST to URL (Django will take over when call hits the "back end")
    dataFactory.postApiData = function (myUrl, myData) {
        return $http.post(myUrl, myData)
            .then(function(response) {
                return response.data;
            },
            function (httpError) {
                throw httpError.status + " : " + httpError.data;
            });
    };

    return dataFactory;
 
});

// Controller for listing threads and submitting threads via form
myApp.controller('threadController', function($scope, $http, dataFactory) {

    // base url to query
    var urlBase = '/threads';
    // alert message
    var myAlertMessage = "You must fill in both Title and Name fields";

    // define fuction which calls factory function to get thread list
    $scope.getThreadlist = function () {
        dataFactory.getApiData(urlBase).then(function(data) { $scope.myThreads = data; });
    }
    // call it
    $scope.getThreadlist();

    // This function will submit the user-provided data in the Create Thread form
    // to the URL /create_post/, at which point the Django view will take over 
    // to add this information into the database
    $scope.submit = function() {

	// if data nonempty
        if ($scope.userthread.mytitle && $scope.userthread.myusername) {
            dataFactory.postApiData('create_post/', $scope.userthread)
	        .then(function(data) {
	            // re-list the threads, since updates have happened
                    $scope.getThreadlist();
	    });

	    // clear the form etc
            $scope.userthread = {};
            $scope.alertMessage = "";
	}
	else {
            $scope.alertMessage = myAlertMessage;
	}
    };

});

// Controller for comments view
myApp.controller('commentController', function($scope, $http, $routeParams, dataFactory) {

    // base url to query
    var urlBase = '/threads';
    // alert message
    var myAlertMessage = "You must fill in both Text and Name fields";

    // grab variable part of URL (i.e., the thread id)
    var threadId = $routeParams.threadid;

    // define fuction which calls factory function to get comment list
    $scope.getCommentlist = function () {
        dataFactory.getApiData(urlBase + '/' + threadId + '/comments/').then(function(data) { $scope.myComments = data; });
    }
    // call it
    $scope.getCommentlist();

    // call factory function to get associated thread
    dataFactory.getApiData(urlBase + '/' + threadId).then(function(data) { $scope.myCommentThread = data; });

    $scope.submit = function() {

	// set thread id of comment
	$scope.usercomment.mythreadid = threadId;

	// if data nonempty
        if ($scope.usercomment.mytext && $scope.usercomment.myusername) {
	    // POST $scope.usercomment JSON to create_comment/ URL
            dataFactory.postApiData('create_comment/', $scope.usercomment)
	        .then(function(data) {
                    // re-list the comments, since updates have happened
                    $scope.getCommentlist();
	        });

            $scope.usercomment = {};
            $scope.alertMessage = "";
	}
	else {
            $scope.alertMessage = myAlertMessage;
	}
    };

    $scope.likeComment = function(commentId) {

	// initialize variable
        $scope.usercomment = {};

	// set comment id of comment
	$scope.usercomment.mycommentid = commentId;

	// POST $scope.usercomment JSON to like_comment/ URL
        dataFactory.postApiData('like_comment/', $scope.usercomment)
	    .then(function(data) {
		// re-list the comments, since updates have happened
                $scope.getCommentlist();
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
        });

    // $locationProvider.html5Mode(true);

});

// Add stuff to header, deal with csrftoken issue
// modified from http://django-angular.readthedocs.org/en/latest/integration.html (see the discussion there)
// and http://www.daveoncode.com/2013/10/17/how-to-make-angularjs-and-django-play-nice-together/
myApp
    .config(function($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    })
    .run(['$http','$cookies', function($http, $cookies) {
            $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;
    }]);
