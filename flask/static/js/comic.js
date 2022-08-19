$(function(){
//***ブラウザ幅取得***
    var width = $(window).width();
    
//***左右開始ページ別処理1***
    if(display === 1){
        $("#first_page").remove();
    }
    
//***パラメータ指定***
    var num = 1;
    
    // URLのパラメータを取得（?p=n）
    var urlParam = location.search.substring(1);
    // URLにパラメータが存在する場合
    if(urlParam) {
      var param = urlParam.split('&');
      var paramArray = [];
      for (i = 0; i < param.length; i++) {
        var paramItem = param[i].split('=');
        paramArray[paramItem[0]] = paramItem[1];
      }
        num = parseInt( paramArray.p );
    }
    
    num = num - 1;
    if(width <= 768){ //768px以下のとき
    } else {//769px以上のとき
        if(display === 1){ //右ページ始まりの時
            if (num % 2 == 0) {// 偶数の処理
            }
            else {// 奇数の処理
                num = num - 1;
            }
        }else { //左ページ始まりの時
            if (num % 2 == 0) {// 偶数の処理
            }
            else {// 奇数の処理
                num = num + 1;	
            }
        }
    }
    
//***slick設定***
    $slider = $('.slider');
    var total_minus = 2;
    
    function sliderSetting(){
        //ブラウザ幅分岐
        if(width <= 768){ //768px以下のときのslickオプション＆イベント
            $slider.slick({
                accessibility: false,
                dots:true,
                appendDots:$('.dots'),
                prevArrow: '<div class="slide-arrow prev-arrow"><span></span></div>',
                nextArrow: '<div class="slide-arrow next-arrow"><span></span></div>',
                slidesToShow:1,
                slidesToScroll:1,
                touchThreshold: 10,
                lazyLoad: 'progressive',
                infinite:false,
                rtl:true,
                initialSlide:num,
            });
            $slider.slick('slickRemove',true); //一枚目削除
            total_minus = 1;
        } else { //769px以上のときのslickオプション＆イベント
            $slider.slick({
                dots:true,
                appendDots:$('.dots'),
                prevArrow: '<div class="slide-arrow prev-arrow"><span></span></div>',
                nextArrow: '<div class="slide-arrow next-arrow"><span></span></div>',
                slidesToShow:2,
                slidesToScroll:2,
                touchThreshold: 10,
                lazyLoad: 'progressive',
                infinite:false,
                rtl:true,
                initialSlide:num,
            });
        }
        //スライド枚数カウント用
        $slider.on('setPosition', function(event, slick) {
            $('.current').text(slick.currentSlide + 1);
            if(display === 1){ //右ページ始まりの時
                $('.total').text(slick.slideCount - total_minus + 1 + "P");
            } else { //左ページ始まりの時
                $('.total').text(slick.slideCount - total_minus + "P");
            }  
        })
        $slider.on('beforeChange', function(event, slick, currentSlide, nextSlide) {
            $('.current').text(nextSlide + 1);
        });
    }
 
    sliderSetting();
    
    $(window).resize( function() {
        sliderSetting();
    });


//***動作設定***
    //最初と最後の矢印のスタイルリセット(cssで非表示)
    $(".slide-arrow.slick-disabled").removeAttr("style");
    
    //もう一度読むボタン
    $(".b_button").click(function(){
        $slider.slick('slickGoTo',0);
    });
    
    //操作ヘルプ表示非表示
    $(".p_button,.help").click(function(){
        $(".help").toggle(300);
    });
    
    //最初にガイド表示
    $(".guide:not(:animated)").fadeIn(function(){
        $(this).delay(5000).fadeOut("fast");
    });
    $(".guide").click(function(){
        $(this).stop().fadeOut("fast");
    });
    $(document).keydown(function(){
        $(".guide").stop().fadeOut("fast");
    });
    
//***拡大モード***
    function zoomSetting(){
        $(".menu_show").slideUp(300);
        $slider.toggleClass("zoom");
        $(".zoomwrap").fadeToggle(300);
        $(".zoom_reset").fadeToggle(300);
        //$("html").scrollLeft(width);
    }
    $(".z_button").click(function(){
        zoomSetting();
    });
    
//***キーボード操作***
    $(document).keydown(function(e) {
        if(e.keyCode === 39){//右　前のページ
            $slider.slick('slickPrev');
        }else if(e.keyCode === 37){//左　次のページ
            $slider.slick('slickNext');
        }else if(e.keyCode === 40){//下　メニュー表示
            $(".menu_show").slideToggle(300);
        }else if(e.keyCode === 38){//上　拡大モード
            zoomSetting();
        }
    });
    
//***全画面表示・非表示***
    //全画面表示振り分け
    Element.prototype.requestFullscreen = Element.prototype[(
        Element.prototype.requestFullscreen ||
        Element.prototype.msRequestFullscreen ||
        Element.prototype.webkitRequestFullScreen ||
        Element.prototype.mozRequestFullScreen ||
        {name:null}).name] || function(){};

    document.exitFullscreen = 
        document.exitFullscreen ||
        document.msExitFullscreen ||
        document.webkitExitFullscreen ||
        document.mozCancelFullScreen ||
        function(){};

    if(!document.fullscreenElement)
        Object.defineProperty(document, "fullscreenElement",{
            get : function(){
                return(
                    document.msFullscreenElement ||
                    document.webkitFullscreenElement ||
                    document.mozFullScreenElement || null);
            }
        });
    //表示非表示
    $(".g_button").click(function(){
        if(!document.fullscreenElement){
            $("body")[0].requestFullscreen();
            $(".g_button").val("全画面解除");
        }else{
            if(document.exitFullscreen){
                document.exitFullscreen();
                $(".g_button").val("全画面表示");
            }
        }
    });
    
//***端末別処理***
	var agent = navigator.userAgent;
    if(agent.search(/iPhone/) != -1 || agent.search(/iPad/) != -1 || agent.search(/iPod/) != -1 || agent.search(/Android/) != -1 || agent.search(/Macintosh/) != -1 && 'ontouchend' in document){
        //***スマホ・タブレット時***
        //指定クラスの要素非表示
        $(".sp_none").hide();
        //menu表示非表示
        $('.menu_box').after('<div class="menu_sizeup"></div>');
        $(".menu_sizeup").click(function(){
            $(".menu_show").slideToggle(300);
        }); 
        $(".menu_button.close").click(function(){
            $(".menu_show").slideUp(300);
        });     
        $slider.click(function(){
            $(".menu_show").slideUp(300);
        });
        //ダブルタップ操作*****拡大モード*****
        var tapCount = 0;
        $(".slider,.zoomwrap").on('touchstart', function(e) {
            if(!$(e.target).closest(".slide-arrow").length) {
                // タッチ範囲に矢印が含まれてない時
                // シングルタップ判定
                if( !tapCount ) {
                    ++tapCount ;
                    setTimeout(function(){
                        tapCount = 0;
                    },300);
                // ダブルタップ判定
                } else {
                    // ブラウザ機能によるズームを防止
                    e.preventDefault(); 
                    //拡大モード
                    zoomSetting();
                    //判定カウントリセット
                    tapCount = 0;
                }
            } else {
                // タッチ範囲に矢印が含まれている時
            }
        });
	}else{
        //***PC時***
        //指定クラスの要素非表示
        $(".pc_none").hide();
        //矢印ホバー処理
        $(".slide-arrow").on('mouseenter',function(){
            $(this).addClass('hover');
        }).on('mouseleave',function(){
            $(this).removeClass('hover');
        });
        //menu表示非表示
        $(".menu_button").click(function(){
            $(".menu_show").slideToggle(300);
        });
        $(".menu_button.close").click(function(){
            $(".menu_show").slideUp(300);
        });
        $slider.click(function(){
            $(".menu_show").slideUp(300);
        });
    }
    
//***左右開始ページ別処理2***
    if(display === 1){
        var width = $(window).width();
        if(width <= 768){ //768px以下のとき
            $slider.slick('slickAdd','<div><div class="c_i"><div><img data-lazy="1.' + imgtype + '" src="../images/load.gif"></div></div></div>',0,'addBefore');
        }
    }
    
});

/***slick-custom***
https://guardian.bona.jp/st/cv/
Licensed under the MIT license.
Copyright (c) 2019 hatsu kyugen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*************/