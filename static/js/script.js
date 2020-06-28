// Scroll.js

$(window).on('popstate',function(e){
	e.preventDefault();
	var target = window.location.href.split("#")[1];
	if(target != "" && target!=undefined && document.getElementById(target)!=null){
		$('html, body').stop().animate({'scrollTop': $("#"+target).offset().top}, 500, 'swing', function () {
			window.location.hash = target;
		});
	}
});

$(document).ready(function() {
	SF_scripts();
});

function SF_scripts(){

	$(window).resize(function(){
		resizeVideo();
		showMenuBtn();
	});

	$(window).trigger("resize");

	// open menu on mobile
	function showMenuBtn(){
		if($(window).width()<1199.98){
			$(".open_menu").addClass("d-block");
			$("header nav").addClass("d-none");
			$(".navigation_mobile").removeClass("opened");
		}else{
			$(".open_menu").removeClass("d-block");
			$("header nav").removeClass("d-none");
			$(".navigation_mobile").removeClass("opened");
		}
	}

	$(".open_menu").click(function(event){
		event.preventDefault();
		$(".navigation_mobile").addClass("opened");
	});

	$(".close_menu, header, section, footer, .navigation_mobile .inner a").click(function(event){
		$(".navigation_mobile").removeClass("opened");
	});
	
	// Set | remove z-index for sections, that has dropdown
	function SF_dropdown_parent(dropdown){
		// Find dropdown's parent nav|header|section|footer
		var section = dropdown;
		var noBreak = true;
		while(noBreak){
			if(
				section[0].tagName=="NAV" || 
				section[0].tagName=="HEADER" || 
				section[0].tagName=="SECTION" || 
				section[0].tagName=="FOOTER" || 
				section[0].tagName=="BODY"
			){
				noBreak = false;
				break;
			}else{
				section = section.parent();				
			}
		}
		return section;
	}
	function SF_highest_zIndex(){
		// Find nav|header|section|footer with highest z-index on page
		var zIndex = 1;
		var currentzIndex;
		var section;
		$("nav, header, section, footer").each(function(){
			currentzIndex = parseInt($(this).css("z-index"));
			if(zIndex < currentzIndex){
				zIndex = currentzIndex;
				section = $(this);
			}
		});
		return [zIndex, section];
	}
	
	// Set highest z-index for section, that has opened dropdown
	$(".dropdown").on("show.bs.dropdown", function () {
		var section = SF_dropdown_parent($(this));
		section.css("z-index",SF_highest_zIndex()[0]+1);	
	});
	
	// Remove z-index for section, where dropdown was closed
	$(".dropdown").on("hidden.bs.dropdown", function () {
		var section = SF_dropdown_parent($(this));
		section.css("z-index","auto");	
	})
	
	// Navigation dropdown popup
	if($(".js-nav-dropdowns").length>0){
		$("body").click(function(event){
			if($(event.target).closest(".navigation_popup").length==0 && $(event.target).closest(".js-open-nav-dropdown").length==0){
				$(".navigation_popup.opened").removeClass("opened");
				$(".js-open-nav-dropdown i.fa-flip-vertical").removeClass("fa-flip-vertical");
			}
		});
		
		$(".js-nav-dropdowns .js-open-nav-dropdown").click(function(event){
			event.preventDefault();
			var id = $(".js-nav-dropdowns .js-open-nav-dropdown").index($(this));
			if($(".navigation_popup").eq(id).hasClass("opened")){
				$(this).find("i").removeClass("fa-flip-vertical");
				$(".navigation_popup").eq(id).removeClass("opened");
			}else{
				$(".navigation_popup.opened").removeClass("opened");
				$(".js-open-nav-dropdown i.fa-flip-vertical").removeClass("fa-flip-vertical");
				$(".navigation_popup").eq(id).addClass("opened");			
				$(this).find("i").addClass("fa-flip-vertical");
				var section = SF_dropdown_parent($(this));
				section.css("z-index",SF_highest_zIndex()[0]+1);				
			}
		});
	}

	// Resize video, saving aspect ratio
	function resizeVideo(){
		var width, height, ratio;
		$(".video").each(function(){
			ratio = $(this).data("ratio");
			ratio = ratio.split("/");
			ratio = ratio[0]/ratio[1];
			width = $(this).width();
			height = width/ratio;
			$(this).height(height);
		});
	}

	resizeVideo();

	// Play video
	$(".video .play").click(function(){
		var video = $(this).parent().parent().find("video");
		$(this).closest(".poster").fadeOut(300,function(){
			video.fadeIn(300,function(){
				video[0].play();
				video[0].onended = function() {
					$(this).parent().find(".poster").delay(100).fadeIn(300);
				};
			});
		});
	});
	
	// Opening tabs
	function openTab(tab){
		if(tab.hasClass("opened")){
			$(".tab_text").animate({height:0},300);
			tab.removeClass("opened");
		}else{
			var nextTabHeight = tab.next().find("div").outerHeight(true);
			$(".tab_text").not(tab.next()).animate({height:0},300);
			tab.next().animate({height:nextTabHeight},300);
			$(".tab_opener").removeClass("opened");
			tab.addClass("opened");
		}
	}

	$(".tab_opener").click(function(){
		openTab($(this));
	});

	if($(".opening_tabs").length > 0){
		$(".tab_opener").each(function(){
			if($(this).hasClass("opened")){
				$(this).removeClass("opened").trigger("click");
			}
		});
	}

	// Copy text from block
	if($("#copy_from_me").length > 0){
		function copyStringToClipboard (str) {
		   var el = document.createElement('textarea');
		   el.value = str;
		   el.setAttribute('readonly', '');
		   el.style = {position: 'absolute', left: '-9999px'};
		   document.body.appendChild(el);
		   el.select();
		   document.execCommand('copy');
		   document.body.removeChild(el);
		}
		$('.js-copy-btn').click(function(){
			copyStringToClipboard ($("#copy_from_me").text());
		});
	}

	/*
		Sliders
	*/
	
	var slick_slider;

	if($(".header_8 .slider").length>0){
		$(".header_8 .slider").each(function(index){
			slick_slider = $(this);
			if(slick_slider.hasClass("slick-initialized")===false){
				slick_slider.slick({
					dots: true,
					arrows: true,
					infinite: true,
					speed: 300,
					slidesToShow: 1,
					slidesToScroll: 1,
					autoplay: true,
					autoplaySpeed: 20000,
					responsive: [
						{
						  breakpoint: 481,
						  settings: {
							arrows:false
						  }
						}
					]
				});
			}
		});
	}

	if($(".header_19 .slider").length>0){
		$(".header_19 .slider").each(function(index){
			slick_slider = $(this);
			if(slick_slider.hasClass("slick-initialized")===false){
				slick_slider.slick({
					dots: true,
					arrows: false,
					infinite: true,
					speed: 300,
					slidesToShow: 1,
					slidesToScroll: 1,
					autoplay: true,
					autoplaySpeed: 20000,
					vertical: true,
					verticalSwiping: true,
					responsive: [
						{
						  breakpoint: 1200,
						  settings: {
							vertical: false,
							verticalSwiping: false
						  }
						}
					]
				});
			}
		});
	}
	
	if($(".navigation_23 .slider").length>0){
		$(".navigation_23 .slider").each(function(index){
			slick_slider = $(this);
			if(slick_slider.hasClass("slick-initialized")===false){
				slick_slider.slick({
					dots: true,
					arrows: false,
					infinite: true,
					speed: 300,
					slidesToShow: 1,
					slidesToScroll: 1,
					autoplay: true,
					autoplaySpeed: 20000,
				});
			}
		});
	}
	if($(".navigation_26 .slider").length>0){
		$(".navigation_26 .slider").each(function(index){
			slick_slider = $(this);
			if(slick_slider.hasClass("slick-initialized")===false){
				slick_slider.slick({
					dots: true,
					arrows: false,
					infinite: true,
					speed: 300,
					slidesToShow: 1,
					slidesToScroll: 1,
					autoplay: true,
					autoplaySpeed: 20000,
				});
			}
		});
	}
	
	if($(".feature_29 .slider").length>0){
		$(".feature_29 .slider").each(function(index){
			slick_slider = $(this);
			if(slick_slider.hasClass("slick-initialized")===false){
				slick_slider.slick({
					dots: true,
					arrows: false,
					speed: 300,
					slidesToShow: 1,
					slidesToScroll: 1,
					vertical:true,
					verticalSwiping:true,
					adaptiveHeight:true,
					responsive: [
						{
						  breakpoint: 767,
						  settings: {
							vertical:false,
							verticalSwiping:false,
						  }
						}
					]
				});
			}
		});
	}

	if($(".feature_31 .slider").length>0){
		$(".feature_31 .slider").each(function(index){
			slick_slider = $(this);
			if(slick_slider.hasClass("slick-initialized")===false){
				slick_slider.slick({
					dots: true,
					arrows: false,
					speed: 300,
					slidesToShow: 1,
					slidesToScroll: 1,
					vertical:true,
					verticalSwiping:true,
					responsive: [
						{
						  breakpoint: 768,
						  settings: {
							vertical:false,
							verticalSwiping:false,
						  }
						}
					]
				});
			}
		});
	}

}; // SF_scripts end
