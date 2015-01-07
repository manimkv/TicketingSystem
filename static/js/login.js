
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
    $http.get("/fetch_tickets/?sort_parm=status", {})
                    .success(function(data) {
                        $scope.list_details = data;
                    });
    $scope.fetch_sorted = function(sort_parm){
        $http.get("/fetch_tickets/?sort_parm="+sort_parm, {})
                    .success(function(data) {
                        $scope.list_details = data;
                    });
    }

    $scope.fetch_filtered = function(filter_parm){
        $http.get("/filter_tickets/?filter_parm="+filter_parm, {})
                    .success(function(data) {
                        $scope.list_details = data;
                    });
    }
    $scope.save_details=function(subject,submitted_date,modified_date,first_response,contact,description,status,assigned_to,priority){
        var data = {}
        data['action']='new';
        data['ticket'] = {
            subject:subject,
            submitted_date:submitted_date,
            modified_date:modified_date,
            first_response:first_response,
            contact:contact,
            description:description,
            status:status,
            assigned_to:assigned_to,
            priority:priority
        }
             $http({ 
    method: 'POST', 
    url: '/ticket_action/', 
    data: data
    }).success(function (data,status) {
        window.location='/dashboard/'
    });
    }
    $scope.change_status=function(val){
        var data = [].concat(val)
        data['action'] ='update';
          $http({ 
            method: 'POST', 
            url: '/ticket_action/', 
            data: data
            }).success(function (data,status) {
                alert(data['subject']+"status updated");
                // window.location='/dashboard/'
            });
    }
    // $scope.list_head = ['lsd','sdfsd','wefwe','sdfds']
    $scope.fields = ['subject','submitted_date','modified_date','first_response','contact','assigned_to','description','status','priority']
    $scope.filters = ['Open', 'Working', 'Closed','Now', 'Soon', 'Someday']

});
