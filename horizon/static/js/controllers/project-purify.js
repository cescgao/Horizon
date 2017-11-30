horizonApp.controller('purifyController', function ($scope, $http, $sce) {
    $scope.toPurify = function () {
        $http.post('/api/project/purify/purify', {url: $scope.url}).success(function (res) {
            http_callback(res, function (data) {
                $scope.pureHtml = data.result;
                $scope.title = data.title;
            })
        });
    };
});