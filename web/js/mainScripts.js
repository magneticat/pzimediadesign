
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
    "min-height": $(window).height()+75+"px"
  })

  $(".isotope").css({
    "min-height": $(window).height()+200+"px"
  })
}

function stickyElements(){
  $('#filter').fixedsticky();
}

function initIsotope(){
  var $container = $('.isotope').isotope({
    masonry: {
      columnWidth: '.grid-sizer'
    },
    transitionDuration: '0.2s',
    filter: hashOptions,    
  });
  
}

function sidebarOff(){
  if($(window).width()>768){
    $(".closeSidebar").css('display','none')
    if($(document).scrollTop()>$('#zwartIntro').height()-1 && $(document).scrollTop()<$("#section03").offset().top){
      $("#sidebarInner").slideDown(0)
    }
  } else {
    if(slideLock == false){
      $("#sidebarInner").slideUp(0)
    }
    $(".closeSidebar").css('display','block')
  }
}

function ifSticky(){
  if (!$("#filter").hasClass('fixedsticky-on')){
    if($(document).scrollTop()>$('#zwartIntro').height()-1 && $(document).scrollTop()<$("#section03").offset().top){
      if(is_chrome){$('#filter').css({'position':'fixed'})}
      if($(window).width()<768){
          $(".closeSidebar").css('display','block')
      if(slideLock == false){
        // $("#sidebarInner").slideDown(0)
      }
      }else{
        $("#sidebarInner").slideDown(200)
      } 
    }else{
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
        $(".closeSidebar").html('<img src="./img/arrowDown.svg"/>')
    }else{
        slideLock = false
        $(".closeSidebar").html('<img src="./img/arrowUp.svg"/>')
    }
});

function toggleDescInner(){ 
    $("#sideBarDescInnerToggle").on('click', function(){
        $("#sideBarDescInner").slideToggle()
    })
}

function initUnderlineFilters(){
    startfilter = window.location.hash.replace('#filters', '')
    startfilterArray = startfilter.split(".")
    startfilterArray.shift()
    startfilterArray.forEach(function(afilter) {
        $('input.'+afilter+'').next("p").toggleClass("underlineFilter")
        moveToSide = $('input.'+afilter+'').next("p").outerWidth()
        $('input.'+afilter+'').parent().next('label').css({"margin-left":moveToSide+"px"})
        $('input.'+afilter+'').prop('checked', $(this).is(':checked'));
        $('input.'+afilter+'').prop( "checked", true )
        $("#sideBarDesc").find($("."+afilter)).prependTo("#sideBarDescInner").slideDown(50)
    });
}

function filterByInput(){
  var $checkboxes = $('.themes input');
  $checkboxes.change( function() {
    $(document).scrollTop($('#section02').offset().top);
    $("#sidebarInner").slideDown(400)
    $('body').css({"opacity":'0'})
    var thisSaved = $(this)
    function layoutComplete(par01){
    $('input.'+par01.attr("class")+'').next("p").toggleClass("underlineFilter")
    $('input.'+par01.attr("class")+'').prop('checked', par01.is(':checked'));
    if ($('input.'+par01.attr("class")+'').next("p").hasClass("underlineFilter")){
        moveToSide = $('input.'+par01.attr("class")+'').next("p").outerWidth()
        foundClass=par01.attr("class")
        $("#sideBarDesc").find($("."+foundClass)).prependTo("#sideBarDescInner").slideDown(50)
    }else{
        moveToSide = 0
        foundClass=par01.attr("class")
        $("#sideBarDesc").find($("."+foundClass)).slideUp(50)
    }
    $('input.'+par01.attr("class")+'').parent().next('label').css({"margin-left":moveToSide+"px"})
    $('body').css({"opacity":'1'})
    }
    var checkboxesCheck = $('.themes input:checked');
    var exclusives = [];
    $checkboxes.each( function( i, elem ) {
    if ( elem.checked ) {
      exclusives.push( elem.value );
    }
    });
    exclusives = exclusives.join('');
    var filterValue;
    filterValue = exclusives;
    location.hash = '#filters'+filterValue
    hashOptions = window.location.hash.replace('#filters', '')
    $container = $('.isotope').isotope({
        filter: hashOptions
    })
    $container.on('layoutComplete', layoutComplete(thisSaved))
  });     
}

// RUN THE FUNCTIONS

windowHeightDivs()
initIsotope()
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


$('html, body').animate({
    scrollTop: $("div.isotope").offset().top
}, 2000);

