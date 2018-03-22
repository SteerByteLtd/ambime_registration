$(document).ready(function() {
	$.backstretch([
		"/static/pages/media/bg/1.jpg",
		"/static/pages/media/bg/2.jpg",
		"/static/pages/media/bg/3.jpg",
		"/static/pages/media/bg/4.jpg"
		], {
		  fade: 1000,
		  duration: 8000
		}
	);

	$("#id_network_provider1").attr("disabled", "disabled");
	$("#id_network_provider2").attr("disabled", "disabled");

	$("#id_landline1").on("change", function(){
		if($(this).val() != "")
			$("#id_network_provider1").removeAttr("disabled");
		else
			$("#id_network_provider1").attr("disabled", "disabled");
	});

	$("#id_landline2").on("change", function(){
		if($(this).val() != "")
			$("#id_network_provider2").removeAttr("disabled");
		else
			$("#id_network_provider2").attr("disabled", "disabled");
	});
});