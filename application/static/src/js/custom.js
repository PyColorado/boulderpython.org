(function ($) {
	"use strict";

	// sticky header
	function StickyHeader () {
		var headerScrollPos = $('header').next().offset().top;
		if($(window).scrollTop() > headerScrollPos) {
			$('header').addClass('header-fixed gradient-overlay');
		}
		else if($(this).scrollTop() <= headerScrollPos) {
			$('header').removeClass('header-fixed gradient-overlay');
		}
	}

	function SmoothMenuScroll () {
		var anchor = $('.scrollToLink');
		if(anchor.length){
			anchor.children('a').bind('click', function (event) {
				var headerH = '95';
				var target = $(this);
				$('html, body').stop().animate({
					scrollTop: $(target.attr('href')).offset().top - headerH + 'px'
				}, 1200, 'easeInOutExpo');
				anchor.removeClass('current');
				target.parent().addClass('current');
				event.preventDefault();
			});
		}
	}

	// // adding active class to menu while scroll to section
	// function OnePageMenuScroll () {
	//     var windscroll = $(window).scrollTop();
	//     if (windscroll >= 100) {
	//     	$('.mainmenu .scrollToLink').find('a').each(function (){
	//     		// grabing section id dynamically
	//     		var sections = $(this).attr('href');
	// 	        $(sections).each(function() {
	// 	        	// checking is scroll bar are in section
	// 	            if ($(this).offset().top <= windscroll + 100) {
	// 	            	// grabing the dynamic id of section
	// 	        		var Sectionid = $(sections).attr('id');
	// 	        		// removing current class from others
	// 	        		$('.mainmenu').find('li').removeClass('current');
	// 	        		// adding current class to related navigation
	// 	        		$('.mainmenu').find('a[href=#'+Sectionid+']').parent().addClass('current');
	// 	            }
	// 	        });
	//     	});
	//     } else {
	//         $('.mainmenu li.current').removeClass('current');
	//         $('.mainmenu li:first').addClass('current');
	//     }
	// }

    // upcoming event filter
    function UpcomingEventFilter () {
    	var UpcomingEventFilterContent = $('#upcoming-event .tab-content-wrap');
    	if (UpcomingEventFilterContent) {
	    	UpcomingEventFilterContent.mixItUp({
	    		load: {
	    		    filter: '.active-event'
	    		}
	    	});
    	};
    }

	function DeadMenuConfig () {
		var deadLink = $('.mainmenu li.deadlink');
		if(deadLink.length) {
			deadLink.each(function () {
				$(this).children('a').on('click', function() {
					return false;
				});
			});
		}
	}

	// revolution slider
	function RevolutionSliderActiver () {
		var banner = $('#banner .banner');
		if (banner.length) {
			banner.revolution({
				delay:5000,
				startwidth:1170,
				startheight:820,
				startWithSlide:0,

				fullScreenAlignForce:"on",
				autoHeight:"off",
				minHeight:"off",

				shuffle:"off",

				onHoverStop:"on",


				hideThumbsOnMobile:"off",
				hideNavDelayOnMobile:1500,
				hideBulletsOnMobile:"off",
				hideArrowsOnMobile:"off",
				hideThumbsUnderResoluition:0,

				hideThumbs:1,
				hideTimerBar:"on",

				keyboardNavigation:"on",

				navigationType:"bullet",
				navigationArrows: "nexttobullets",
				navigationStyle:"preview4",

				navigationHAlign:"center",
				navigationVAlign:"bottom",
				navigationHOffset:30,
				navigationVOffset:30,

				soloArrowLeftHalign:"left",
				soloArrowLeftValign:"center",
				soloArrowLeftHOffset:20,
				soloArrowLeftVOffset:0,

				soloArrowRightHalign:"right",
				soloArrowRightValign:"center",
				soloArrowRightHOffset:20,
				soloArrowRightVOffset:0,


				touchenabled:"on",
				swipe_velocity:"0.7",
				swipe_max_touches:"1",
				swipe_min_touches:"1",
				drag_block_vertical:"false",

				parallax:"mouse",
				parallaxBgFreeze:"on",
				parallaxLevels:[10,7,4,3,2,5,4,3,2,1],
				parallaxDisableOnMobile:"off",

				stopAtSlide:-1,
				stopAfterLoops:-1,
				hideCaptionAtLimit:0,
				hideAllCaptionAtLilmit:0,
				hideSliderAtLimit:0,

				dottedOverlay:"none",

				spinner: 'spinner0',

				lazyType: "smart",

				fullWidth:"on",
				forceFullWidth:"on",
				fullScreen:"off",
				fullScreenOffsetContainer:"#banner",
				fullScreenOffset:"0px",

				panZoomDisableOnMobile:"off",

				simplifyAll:"off",

				shadow:0

			});
		};
	}

	// wow activator
	function wowActivator () {
		var wow = new WOW ({
    		offset: 0
    	});
    	wow.init();
	}

	// mobile menu config
	function mobileMenuConfig () {
		var menuContainer = $('nav.mainmenu-container');
		if (menuContainer.length) {
			menuContainer.find('ul .dropdown').children('a').append(function () {
				return '<i class="fa fa-bars"></i>';
			});
			menuContainer.find('.fa').on('click', function () {
				$(this).parent().parent().children('ul').slideToggle(300);
				return false;
			});
			menuContainer.find('.nav-toggler').on('click', function () {
				// $(this).parent().children('ul').slideToggle();
				$(this).toggleClass('active');
   				$('#navoverlay').toggleClass('open');
			});
		};
	}

	// subscribe email
	function NewsletterSubscribe () {
		$("#subscribe").on('click', function () {
			var email = $("#newsletter-email").val();
			$.ajax({
				type: "POST",
				url: "/subscribe",
				data: JSON.stringify({'email': email}),
				contentType: 'application/json',
				success:function(data) {
				    $("#newsletter-email").val("");
				},
				error: function(data) {
					console.log(data);
				    $("#newsletter-email").val("");
				},
			})
		});
	}

	// doc ready
	$(document).on('ready', function () {
		SmoothMenuScroll();
		UpcomingEventFilter();
		DeadMenuConfig();
		RevolutionSliderActiver();
		wowActivator();
		mobileMenuConfig();
		NewsletterSubscribe();
	});

	// window load
	$(window).on('load', function () {});

	// window scroll
	$(window).on('scroll', function () {
		StickyHeader();
		// OnePageMenuScroll();
	});

})(jQuery);