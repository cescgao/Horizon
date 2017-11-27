horizonApp.directive('ngThumb', ['$window', function($window) {
    var helper = {
        support: !!($window.FileReader && $window.CanvasRenderingContext2D),
        isFile: function(item) {
            return angular.isObject(item) && item instanceof $window.File;
        },
        isImage: function(file) {
            var type =  '|' + file.type.slice(file.type.lastIndexOf('/') + 1) + '|';
            return '|jpg|png|jpeg|bmp|gif|'.indexOf(type) !== -1;
        }
    };

    return {
        restrict: 'A',
        template: '<canvas/>',
        link: function(scope, element, attributes) {
            if (!helper.support) return;

            var params = scope.$eval(attributes.ngThumb);

            if (!helper.isFile(params.file)) return;
            if (!helper.isImage(params.file)) return;

            var canvas = element.find('canvas');
            var reader = new FileReader();

            reader.onload = onLoadFile;
            reader.readAsDataURL(params.file);

            function onLoadFile(event) {
                var img = new Image();
                img.onload = onLoadImage;
                img.src = event.target.result;
            }

            function onLoadImage() {
                var width = params.width || this.width / this.height * params.height;
                var height = params.height || this.height / this.width * params.width;
                canvas.attr({ width: width, height: height });
                canvas[0].getContext('2d').drawImage(this, 0, 0, width, height);
            }
        }
    };
}]);
horizonApp.controller('blogCtrl', function($scope, $http, FileUploader){
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
    var reg = window.location.pathname.match(/\d+/g);
    $scope.id = 0;
    if (reg) $scope.id = reg[0];
    if ($scope.id){
        $http.get('/api/axis/edit?id=' + $scope.id).success(function(res){
            http_callback(res, function(data){
                $scope.title = data.title;
                $scope.date = data.date;
                $scope.image = data.image;
                $scope.raw_desc = data.desc;
                $scope.desc = md.render(data.desc);
                $scope.key = data.key;
                if (!$scope.image){
                    $('.blog-single-img').css({display: "none"})
                }
                $('#md-textarea').markdown({
                    onShow: function(e){
                        e.setContent($scope.raw_desc)
                    },
                    onPreview: function(e){
                        return md.render(e.getContent());
                    },
                    onChange: function(e){
                        $scope.raw_desc = e.getContent();
                    }
                });
            });
        });
    }
    $scope.counter = 0;
    var mode = true;
    $scope.show = true;
    $scope.uploader = new FileUploader({
        url: '/api/axis/upload',
        onAfterAddingFile: function(item){
            this.queue.length = 0;
            this.queue.push(item);
            $scope.counter ++;
        },
        onCancelItem: function(item){
            $('.blog-upload-img').animate({opacity: 0, height: 0}, 1000, function(){
                $('.blog-upload-img').css({display: "none"});
            });
            $('.blog-single-img').css({opacity: 0, display: "block", height: "100%"}).animate({opacity: 1}, 1000);
            mode = true;
        },
        onSuccessItem: function(item, response){
            $('.blog-upload-img').animate({opacity: 0, height: 0}, 1000, function(){
                $('.blog-upload-img').css({display: "none"});
            });
            $('.blog-single-img').css({opacity: 0, display: "block", height: "100%"}).animate({opacity: 1}, 1000);
            mode = true;
            http_callback(response, function(data){
                $scope.image = data.url;
                $scope.key = data.key;
            });
        }
    });
    $scope.click = function(){
        $('#upload-button').click();
    };
    $scope.queue = $scope.uploader.queue;
    $scope.$watch('counter', function(event){
        if (event && mode){
            $('.blog-single-img').animate({opacity: 0, height: 0}, 1000, function(){
                $('.blog-single-img').css({display: "none"});
            });
            $('.blog-upload-img').css({opacity: 0, display: "block", height: 0}).animate({opacity: 1, height: "100%"}, 1000);
            mode = false;
        }
    });
    $scope.progress_style = function(item){
        return {width: item.progress + '%'};
    };
    $scope.submit = function(){
        if (!$scope.title){
            sweetAlert('Miss Params', 'Need title', 'error');
        }
        else if (!$scope.key){
            sweetAlert('Miss Params', 'Need image', 'error');
        }
        else if (!$scope.raw_desc){
            sweetAlert('Miss Params', 'Need content', 'error');
        }
        else {
            $http.post('/api/axis/edit', {
                    title: $scope.title, image: $scope.key, desc: $scope.raw_desc, id: $scope.id
                }
            ).success(function(res){
                http_callback(res, function(data){
                    top.location.href = '/axis/blog/' + data.id;
                })
            });
        }
    };
    $scope.cancel = function() {
        if ($scope.id)
            top.location.href = '/axis/blog/' + $scope.id;
        else
            top.location.href = '/axis';
    };
});