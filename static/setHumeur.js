/*Script to set a mood */
function setHumeur(){

	select = document.getElementById("comboselect");
	choice = select.selectedIndex;
	var value = select.options[choice].value;
	var text = select.options[choice].text;

	console.log(value);
	//console.log(text);
	
	var info_sent={
		'humeur': value,
		'music': Player.getAttribute('data-info-Artist') + "-"+Player.getAttribute('data-info-Album-Title')+"-" +Player.getAttribute('data-info-Title')
	};

	console.log(info_sent['music']);
	$.ajax({
	type: 'POST',
	url: '/api/humeur',
	data: JSON.stringify(info_sent),         
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

function div_afficher_masque(){
	var toto = document.getElementById("toto");
	var titi = document.getElementById("titi");
	var icon = document.getElementById("icon_pm");
	
	
	if(toto.style.display == "none"){
	toto.style.display = "block";
	var text = titi.innerText || titi.textContent ;
	console.log(text);
	titi.Title = "Voir moins de musiques";
	titi.innerHTML = "Voir moins de musiques";
	icon.classeName = "glyphicon glyphicon-minus";
	
	
	
	}
	else{
		toto.style.display = "none";
		titi.Title = "Voir plus de musiques";
		titi.innerHTML = "Voir plus de musiques";
		icon.classeName ="glyphicon glyphicon-plus";
		
	}
}

