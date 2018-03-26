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

	$("#id_landline1").blur(function(){
		var phone_number = $(this).val();
		if(phone_number.search(/^[0-9]{3} [0-9]{4} [0-9]{4}$/) == -1) {
            var formatted_number = phone_number.substr(0, 3) + " " + phone_number.substr(3, 4) + " " + phone_number.substr(7, 4);
            $(this).val(formatted_number);
        }
	});

	$("#id_landline2").blur(function(){
		var phone_number = $(this).val();
		if(phone_number.search(/^[0-9]{3} [0-9]{4} [0-9]{4}$/) == -1) {
            var formatted_number = phone_number.substr(0, 3) + " " + phone_number.substr(3, 4) + " " + phone_number.substr(7, 4);
            $(this).val(formatted_number);
        }
	})
});