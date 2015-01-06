var app = angular.module('loginapp', ['ngCookies','ngResource']);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
app.run(function($rootScope, $http, $cookies){
    // set the CSRF token here
    $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;

  });

app.directive('ngEnter', function() {
        return function(scope, element, attrs) {
            element.bind("keydown keypress", function(event) {
                if(event.which === 13) {
                        scope.$apply(function(){
                                scope.$eval(attrs.ngEnter);
                        });
                        
                        event.preventDefault();
                }
            });
        };
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
