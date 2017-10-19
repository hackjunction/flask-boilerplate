$(document).ready(function() {

var controller = new ScrollMagic.Controller({
	globalSceneOptions: {
		triggerHook: 'onEnter'
	}
});

var tl = new TimelineLite();
var logo = $("#nav-logo");
var nav_1 = $("#nav_1");
var nav_2 = $("#nav_2");
var nav_3 = $(".nav_3");
var header = $(".page-header");

var body = $(".main-body-content");


/*TweenMax.to(logo, 0.5, {autoAlpha:1});
TweenMax.to(logo, 0.5, {autoAlpha:1, scale:"3", delay: "0.5"});

to(logo, 0.2, {autoAlpha:1, scale:"1"})

TweenMax.staggerTo([nav_1, nav_2, nav_3], 0.5, {autoAlpha:1}, 0.25);*/



/*var scene = new ScrollMagic.Scene({triggerElement: "#trigger1"})
	.setPin("#nav-logo")
	.setTween(logo, 0.2, {autoAlpha:1, scale:"1"}) // trigger a TweenMax.to tween
	.addTo(controller);

*/

var startingTween = tl.staggerTo([nav_1, nav_2, nav_3, header, body], 0.2, {autoAlpha:1, delay: "0.5"}, 0.2)
	




});