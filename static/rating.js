function rating(item){
	Player=document.getElementById("Player");
	var info_send={
		'note': item['selector'].split('-')[1],
		'music': Player.getAttribute('data-info-Artist') + "-"+Player.getAttribute('data-info-Album-Title')+"-" +Player.getAttribute('data-info-Title')
	};
	console.log(info_send.note);
	console.log(info_send.music);
	$.ajax({
		type: 'POST',
		url: '/api/note',
		data: JSON.stringify(info_send),         
		dataType: 'json',
		contentType: 'application/json; charset=utf-8', 
		success: function(data) {
			console.log("succes")
		},
		error: function(data) {
			console.log("erreur")
		}
		});
}



["#rating-5", "#rating-4", "#rating-3", "#rating-2", "#rating-1"].forEach(function(item){
	$(item).on("click", function(event){
		rating($(item));
	});
});
