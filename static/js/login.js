var app = angular.module('loginapp', ['ngCookies','ngResource']);


app.run(function($rootScope, $http, $cookies){
    // set the CSRF token here
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  });
app.controller('loginController',function ($scope,$http) {
	$scope.continue_login = function(username,password){
		console.log(username,password)
		var data = {email:username,password:password}
		 $http({ 
    method: 'POST', 
    url: '/login/', 
    data: data
    }).success(function (data,status) {
    	window.location='/dashboard/'
    });
	}
});
