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

            // Use the server result to set the post result.
            if (data.result == 1) {
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

function showMoreSongs() {
    var moreThanFiveDiv = document.getElementById("moreThanFiveDiv");
    var showMoreText = document.getElementById("showMoreText");
    var icon = document.getElementById("icon_pm");


    if (moreThanFiveDiv.style.display == "none") {
        moreThanFiveDiv.style.display = "block";
        //var text = showMoreText.innerText || showMoreText.textContent;
        //console.log(text);
        showMoreText.Title = showMoreText.innerHTML = "See less music";
        icon.classeName = "glyphicon glyphicon-minus";
    }
    else {
        moreThanFiveDiv.style.display = "none";
        showMoreText.Title = showMoreText.innerHTML = "See more music";
        icon.classeName = "glyphicon glyphicon-plus";
    }
}

