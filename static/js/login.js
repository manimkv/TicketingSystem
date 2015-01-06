var app = angular.module('loginapp', ['ngCookies','ngResource']);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
app.run(function($rootScope, $http, $cookies){
    // set the CSRF token here
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  });
app.controller('loginController',function ($scope,$http,$cookies) {
	$scope.continue_login = function(username,password){
        $http.defaults.headers.post['csrf_tocken'] = $cookies.csrftoken;
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
    // $scope.list_head = ['lsd','sdfsd','wefwe','sdfds']
    $scope.colors = ['subject','submitted_date','modified_date','first_response','contact','assigned_to','description','status','priority']
});
