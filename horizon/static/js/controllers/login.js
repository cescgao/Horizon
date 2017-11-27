horizonApp.controller('loginController', function($scope, $http){
    $scope.processLogin = function(){
        $('.login').addClass('test');
        setTimeout(function () {
	        $('.login').addClass('testtwo');
	    }, 300);
        setTimeout(function () {
	        $('.authent').show().animate({ right: -320 }, {
	            easing: 'easeOutQuint',
	            duration: 600,
	            queue: false
	        });
	        $('.authent').animate({ opacity: 1 }, {
	            duration: 200,
	            queue: false
	        }).addClass('visible');
	    }, 500);
        $http.post('/api/account/login', $scope.formData).success(function(res){
            setTimeout(function () {
                $('.authent').show().animate({ right: 90 }, {
                    easing: 'easeOutQuint',
                    duration: 600,
                    queue: false
                });
                $('.authent').fadeOut(123);
                $('.login').removeClass('testtwo');
            }, 2500);
            http_callback(res, function(data){
                setTimeout(function () {
                    $('.login').removeClass('test');
                    $('.login div').fadeOut(123);
                }, 2800);
                setTimeout(function () {
                    $('.success').fadeIn();
                }, 3200);
                setTimeout(function(){
                    top.location.reload();
                }, 4000);
            }, function(err){
                setTimeout(function () {
                    $('.login').removeClass('test');
                    $('.failure').show()
                }, 2800);
            });
        });
    };
});