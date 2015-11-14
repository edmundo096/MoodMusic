jQuery(document).ready(function($){
	$('.musique').click(function(){
		console.log($(this))
		var musiques=$(this).text().split(" - ");
		console.log(musiques)
		$.ajax({                                  
			url: "/chercher?titre="+musiques[1].replace(" ","+")+"&compositeur="+musiques[0].replace(" ","+"),
			success: function(music) {         
				document.getElementById("audiosrc").src=music.musicPath;
				var lecteur=document.getElementById("Player")
				lecteur.dataset.infoAlbumArt=music.imagePath;
				lecteur.dataset.infoAlbumTitle=music.album;
				lecteur.dataset.infoArtist=music.compositeur;
				lecteur.dataset.infoTitle=music.titre;
				lecteur.dataset.infoLabel=music.label;
				lecteur.dataset.infoYear=music.annee;

			},
			error: function() {
				console.log("Error");
			}	
		});
		PlayerAudio($)
	})
	
})

/*function ChargerMusique($){
	console.log($('.musique'))
	var musiques=element.innerHTML.split(" - ");
	console.log("ca marche");
	$.ajax({                                  
		url: "/chercher?titre="+musiques[1].replace(" ","+")+"&compositeur="+musiques[0].replace(" ","+"),
		success: function(music) {         
			document.getElementById("audiosrc").src=music.musicPath;
			var lecteur=document.getElementById("Player")
			lecteur.dataset.infoAlbumArt=music.imagePath;
			lecteur.dataset.infoAlbumTitle=music.album;
			lecteur.dataset.infoArtist=music.compositeur;
			lecteur.dataset.infoTitle=music.titre;
			lecteur.dataset.infoLabel=music.label;
			lecteur.dataset.infoYear=music.annee;
			
			
		},
		error: function() {
			console.log("Error");
		}	
	});
	
	
}*/

