function submitPassword(){

	select = document.getElementById("submit_password");
	var password = select.value;

	var info_sent={
		'psswd': password		
	};

	$.ajax({
	type: 'POST',
	url: '/submit_password',
	data: JSON.stringify(info_sent),         
	dataType: 'json',
	contentType: 'application/json; charset=utf-8', 
		success: function(data) {
			console.log("succes submitting new password")
			alert("Password changed")
		},
		error: function(data) {
			console.log("erreur submitting new password")
			alert("Error submitting new password")
		}
	});

	

}