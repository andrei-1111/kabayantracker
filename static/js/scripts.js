$(document).ready(function() {	
	
	$('.dropdown').each(function () {
		$(this).parent().eq(0).hoverIntent({
			timeout: 100,
			over: function () {
				var current = $('.dropdown:eq(0)', this);
				current.slideDown(300);
			},
			out: function () {
				var current = $('.dropdown:eq(0)', this);
				current.fadeOut(100);
			}
		});
	});
	
});