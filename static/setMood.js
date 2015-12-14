/*Script to set a mood */
function setMood() {

    var select = document.getElementById("comboselect");
    var choice = select.selectedIndex;
    var value = select.options[choice].value;
    var text = select.options[choice].text;

    console.log(value);
    //console.log(text);

    // Check if the value is empty.
    if (value == '')
        return;

    var player = $('#player');

    var info_sent = {
        mood: value,
        artist: player.attr('data-info-artist'),
        album: player.attr('data-info-album-title'),
        title: player.attr('data-info-title')
    };

    console.log(info_sent);

    $.ajax({
        type: 'POST',
        url: '/api/mood',
        data: JSON.stringify(info_sent),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            console.log("setMood success");

            if (data.success == 1) {
                var oldSelectedText = select.options[select.selectedIndex].text;
                select.selectedIndex = 0;
                select.options[0].text = oldSelectedText + ' saved';
            }
        },
        error: function (data) {
            console.log("setMood error");
        }
    });
}

function div_afficher_masque() {
    var toto = document.getElementById("toto");
    var titi = document.getElementById("titi");
    var icon = document.getElementById("icon_pm");


    if (toto.style.display == "none") {
        toto.style.display = "block";
        var text = titi.innerText || titi.textContent;
        console.log(text);
        titi.Title = "Voir moins de musiques";
        titi.innerHTML = "Voir moins de musiques";
        icon.classeName = "glyphicon glyphicon-minus";
    }
    else {
        toto.style.display = "none";
        titi.Title = "Voir plus de musiques";
        titi.innerHTML = "Voir plus de musiques";
        icon.classeName = "glyphicon glyphicon-plus";
    }
}

