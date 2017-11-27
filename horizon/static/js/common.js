function formatJson(json) {
    var i = 0, len = 0, tab = "&nbsp&nbsp&nbsp&nbsp", targetJson = "", indentLevel = 0, inString = false, currentChar = null;

    for (i = 0, len = json.length; i < len; i += 1) {
        currentChar = json.charAt(i);

        switch (currentChar) {
            case '{':
                if (!inString) {
                    targetJson += currentChar + "<br />" + repeat(tab, indentLevel + 1);
                    indentLevel += 1;
                } else {
                    targetJson += currentChar;
                }
                break;
            case '[':
                if (!inString) {
                    targetJson += currentChar + "<br />" + repeat(tab, indentLevel + 1);
                    indentLevel += 1;
                } else {
                    targetJson += currentChar;
                }
                break;
            case '}':
                if (!inString) {
                    indentLevel -= 1;
                    targetJson += "<br />" + repeat(tab, indentLevel) + currentChar;
                } else {
                    targetJson += currentChar;
                }
                break;
            case ']':
                if (!inString) {
                    indentLevel -= 1;
                    targetJson += "<br />" + repeat(tab, indentLevel) + currentChar;
                } else {
                    targetJson += currentChar;
                }
                break;
            case ',':
                if (!inString) {
                    targetJson += ",<br />" + repeat(tab, indentLevel);
                } else {
                    targetJson += currentChar;
                }
                break;
            case ':':
                if (!inString) {
                    targetJson += ": ";
                } else {
                    targetJson += currentChar;
                }
                break;
            default:
                targetJson += currentChar;
                break;
        }
    }
    return targetJson;
}


var http_callback = function(data, callback, errorback){
    if (data.code){
        if (errorback == undefined)
            sweetAlert('服务器好累', data.message, 'error');
        else
            errorback(data);
    } else {
        callback(data.data);
    }
};


var http_error = function(data, status, headers, config) {
    sweetAlert('http code', status + '', 'error');
};

var horizonApp = angular.module('horizonApp', ['ngAnimate', 'ngSanitize', 'ui.bootstrap', 'angularFileUpload']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

(function($) {
"use strict";
	$(window).load(function() {
		// will fade loading animation
		$("#object").delay(600).fadeOut(300);
		// will fade loading background
		$("#loading").delay(1000).fadeOut(500);
	})
})(jQuery);

$(document).ready(function(){
    $('.navbar-right i').hover(function(){
        $(this).parent().find('.qrcode').fadeIn();
    }, function() {
        $(this).parent().find('.qrcode').fadeOut();
    });
});