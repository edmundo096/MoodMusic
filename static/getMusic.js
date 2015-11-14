function getMusic(item){
	var info_send={
		'music': item.target.innerHTML.split("> ")[1].substring(0,item.target.innerHTML.split("> ")[1].length-1)
	};
	console.log(item.target.innerHTML.split("> ")[1].substring(0,item.target.innerHTML.split("> ")[1].length-1))
	$.ajax({
		type: 'POST',
		url: '/api/getMusic',
		data: JSON.stringify(info_send),         
		dataType: 'json',
		contentType: 'application/json; charset=utf-8', 
		success: function(data) {
			Player.pause();
			document.getElementById("audiosrc").src=data.musicPath
			
			Player=document.getElementById("Player");
			Player.setAttribute('data-info-Title',data.Titre)
			Player.setAttribute('data-info-Album-Title', data.Album)
			Player.setAttribute('data-info-Artist', data.Artist)
			Player.setAttribute('data-info-Label', data.Label)
			Player.setAttribute('data-info-Year', data.Annee)
			Player.setAttribute('data-info-Album-Art', data.imagePath)
			document.getElementsByClassName("thumbnail")[0].src=data.imagePath
			tableau=document.getElementsByClassName("table table-condensed")[0]
			elements=tableau.getElementsByTagName('td')
			elements[0].innerHTML=data.Artist
			elements[1].innerHTML=data.Titre
			elements[2].innerHTML=data.Album
			elements[3].innerHTML=data.Label
			elements[4].innerHTML=data.Annee
			Player.load();
			Player.play();
			
		},
		error: function(data) {
			console.log("erreur")
		}
		});
	
}
