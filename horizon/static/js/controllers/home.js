/* ==========================
   SMOOTH-SCROLLING
=============================*/
var $scroll_list = ['#tf-page-header', '#about', '#resume', '#services', '#contact'];
var $scrollTarget = 0;
var $scrollClick = function(){
    $(".scroll li.active").removeClass('active');
    $(".scroll li:eq(" + $scrollTarget + ")").addClass('active');
};
var min = 100000;
for (var i = 0;i < $scroll_list.length; i++) {
    if (Math.abs($($scroll_list[i])[0].getBoundingClientRect().top) < min){
        min = Math.abs($($scroll_list[i])[0].getBoundingClientRect().top);
        $scrollTarget = i;
        $scrollClick();
    }
}
var $scrollDelta = 0;
var $scrollEvent = function(event, delta){
    $scrollDelta += delta;
    if ($scrollDelta > 0){
        if ($scrollTarget == 0){
            $scrollDelta = 0;
        }
        else if ($($scroll_list[$scrollTarget - 1])[0].getBoundingClientRect().top + $($scroll_list[$scrollTarget - 1]).outerHeight() >= 0){
            if ($scrollDelta > 1){
                $scrollTarget -= 1;
                $scrollDelta = 0;
                $("a.scroll:eq(" + $scrollTarget + ")").click();
            }
        }
        else {
            $scrollDelta = 0;
            $('body').animate({scrollTop: $(window).scrollTop() - 30}, 10);
        }
    }
    else {
        if ($scrollTarget == $scroll_list.length - 1){
            $scrollDelta = 0;
        }
        else if ($($scroll_list[$scrollTarget + 1])[0].getBoundingClientRect().top - 30 <= $(window).height()) {
            if ($scrollDelta < -1){
                $scrollTarget += 1;
                $scrollDelta = 0;
                $("a.scroll:eq(" + $scrollTarget + ")").click();
            }
        }
        else {
            $scrollDelta = 0;
            $('body').animate({scrollTop: $(window).scrollTop() + 30}, 10);
        }
    }
};
$(document).ready(function(){
    $('.scroll li').hover(function(){
        $(this).find('span.title').animate({
            opacity: 1
        });
    }, function(){
        $(this).find('span.title').animate({
            opacity: 0
        });
    }).click(function(){
        $(this).find('a').click();
    });
});
$(function() {
    "use strict";
    $("a[href^='#']:not(a[href='#'])").click(function() {
        var cur = $(this).attr('href');
        $scroll_list.forEach(function(item, index){
            if (cur == item){
                $scrollTarget = index;
                $scrollClick();
            }
        });
        $scrollDelta = 0;
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                return false;
            }
        }
    });
});

horizonApp.controller('homeCtrl', function($scope, $http){
    $http.get('/api/home/blog').success(function(res){
        http_callback(res, function(data){
            $scope.blog = data;
        });
    });
});