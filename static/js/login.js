
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
		var data = {email:username,password:password}
		 $http({ 
    method: 'POST', 
    url: '/login/', 
    data: data
    }).success(function (data,status) {
    	window.location='/dashboard/'
    });
	}
    $scope.load_avg_res=function(who,month){
        $http.get("/avg_response_tickets/?username="+who+"&&year=2015&&month="+month, {})
                    .success(function(data) {
                        if(month==''){
                        $scope.avg_details = data;
                        }
                        else{
                            $scope.avg_month = data;
                        }
                    });
    }
    $scope.load_avg_res_close=function(who,month){
        $http.get("/avg_closed_tickets/?username="+who+"&&year=2015&&month="+month, {})
                    .success(function(data) {
                        if(month==''){
                        $scope.avg_details_close = data;
                        }
                        else{
                            $scope.avg_details_close_month = data;
                        }
                    });
    }

    $scope.search_tickets=function(query){
        $http.get("/search_tickets/?query="+query, {})
                    .success(function(data) {
                        $scope.list_details = data;
                    });
    }

    $http.get("/fetch_tickets/?sort_parm=status", {})
                    .success(function(data) {
                        $scope.list_details = data;
                    });
    $http.get("/fetch_developers/", {})
                    .success(function(data) {
                        $scope.list_developers = data;
                        $scope.all_developers = $scope.list_developers;
                        $scope.all_developers.push('all')
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
    $scope.save_details=function(subject,contact,description,status,assigned_to,priority){
        var data = {}
        data['action']='new';
        data['ticket'] = {
            subject:subject,
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
        var data = {'status':val['status'],'id':val['id'],'action':'update'}
        // data['action'] ='update';
          $http({ 
            method: 'POST', 
            url: '/ticket_action/', 
            data: data
            }).success(function (data,status) {
                alert(val['subject']+" status updated");
                // window.location='/dashboard/'
            });
    }
    // $scope.list_head = ['lsd','sdfsd','wefwe','sdfds']
    $scope.fields = ['subject','submitted_date','modified_date','first_response','contact','assigned_to','description','status','priority']
    $scope.filters = ['Open', 'Working', 'Closed','Now', 'Soon', 'Someday']

});
