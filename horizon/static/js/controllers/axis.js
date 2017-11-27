horizonApp.controller('axisCtrl', function($scope, $http, $timeout){
    var md = markdownit({
        highlight: function (str, lang) {
            if (lang && hljs.getLanguage(lang)) {
                var code = '';
                str.split('\n').forEach(function(s){
                    if (s)
                        code += '<li><code>' + hljs.highlight(lang, s, true).value + '</code></li>';
                });
                return '<pre class="hljs language-' + lang.toLowerCase() + '"><ol class="linenums">' + code + '</ol></pre>';
            }
            else{
                return '<pre class="hljs"><code>' + md.utils.escapeHtml(str) + '</code></pre>';
            }
        }
    });
    $http.get('/api/axis/list').success(function(res){
        http_callback(res, function(data){
            $scope.points = data;
            $scope.points.forEach(function(item, i){
                if (item.rows)
                    item.rows.forEach(function(_item, _i){
                        _item.desc = md.render(_item.desc);
                    });
            });
        });
    }).error(http_error);
    $timeout(function(){
        $('.VivaTimeline').vivaTimeline({
            carousel: true,
            carouselTime: 3000,
            callback: function(_container, target){
                var title = _container.closest('.events-footer').siblings('.events-body').find('.row').eq(target).attr('title');
                _container.closest('.events-footer').siblings('.events-header').html(title);
            }
        });
    })
});