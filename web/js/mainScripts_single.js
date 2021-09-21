// DEFINE GLOBAL VARIABLES

var hashOptions;
hashOptions = window.location.hash.replace('#filters', '')
var is_chrome = /chrome/i.test( navigator.userAgent );
var slideLock = false;
var isMobile = {
  Android: function() {
    return navigator.userAgent.match(/Android/i);
  },
  BlackBerry: function() {
    return navigator.userAgent.match(/BlackBerry/i);
  },
  iOS: function() {
    return navigator.userAgent.match(/iPhone|iPad|iPod/i);
	},
  Opera: function() {
    return navigator.userAgent.match(/Opera Mini/i);
  },
  Windows: function() {
    return navigator.userAgent.match(/IEMobile/i);
  },
  any: function() {
    return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
  }
};

// DEFINE FUNCTIONS

function windowHeightDivs(){
	if(!isMobile.any()){
		$("#logoWrap").css({"margin-top":$(window).height()-$("#logoWrap").outerHeight()-10+"px"})
	}
	$(".zwartArea").css({
		"min-height": $(window).height()+"px"
	})
}


function stickyElements(){
	$('#filter').fixedsticky();
}


function sidebarOff(){
	if($(window).width()>768){
		$(".closeSidebar").css('display','none')
		$("#sidebarInner").slideDown(0)
	} else {
    if(slideLock == false){
      $("#sidebarInner").slideUp(0)
    }
		$(".closeSidebar").css('display','block')
	}
}

function ifSticky(){
	if (!$("#filter").hasClass('fixedsticky-on')){
		if($(document).scrollTop()>$('#zwartIntro').height()-1){
			if(is_chrome){$('#filter').css({'position':'fixed'})}
			if($(window).width()<768){
				$(".closeSidebar").css('display','block')
			if(slideLock == false){
				// $("#sidebarInner").slideDown(0)
			}
			}else{
				$("#sidebarInner").slideDown(200)
			}	
		} else{
			if(is_chrome){$('#filter').css({'position':''})}
			if($(window).width()<768){	
				$(".closeSidebar").css('display','none')
				if(slideLock == false){
					$("#sidebarInner").slideUp(0)
				}
			}else{
				$("#sidebarInner").slideUp(200)
			}
		}	
	}

}

$(".closeSidebar").click(function(){
  $("#sidebarInner").slideToggle()
  if(slideLock == false){
    slideLock = true
    $(".closeSidebar").html('<img src="../img/arrowDownW.svg"/>')
  }else{
    slideLock = false
    $(".closeSidebar").html('<img src="../img/arrowUpW.svg"/>')
  }
});

function toggleDescInner(){	
	$("#sideBarDescInnerToggle").on('click', function(){
		$("#sideBarDescInner").slideToggle()
	})
}

$('#filter').hover(function(){
    $('.hoverBack').text("Return to index page");
}, function() {
    $('.hoverBack').text("PZI: Master Media Design & Communication");
});


// RUN THE FUNCTIONS

windowHeightDivs()
stickyElements()
toggleDescInner()
sidebarOff()

document.onscroll = function() {
   ifSticky()
};

$( window ).resize(function() {
	windowHeightDivs()
	sidebarOff()
})
