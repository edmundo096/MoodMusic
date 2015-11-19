
/*Script to submit a Picture */
function submitPicture(){

	select = document.getElementById("submit_picture");
	var url = select.value;

	console.log(url)
	url = url.encode()


	var info_sent={
		'picture': url
	};


	$.ajax({
	type: 'POST',
	url: '/submit_picture',
	data: JSON.stringify(info_sent),         
	dataType: 'json',
	contentType: 'application/json; charset=utf-8', 
		success: function(data) {
			console.log("succes submitting new picture")
			alert("Picture submitted")
		},
		error: function(data) {
			console.log("erreur submitting picture")
			alert("Error submitting picture")
		}
	});

	

}