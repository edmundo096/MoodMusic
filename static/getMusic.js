var ytPlayer;

function getMusic(element) {
    element = $(element);
    var info_send = {
        //method: 'info',   // TODO possible method to get the song data: song 'info' or song 'id'
        artist: element.data('artist'),
        album: element.data('album'),
        title: element.data('title')
    };

    console.log(info_send);

    $.ajax({
        type: 'GET',
        url: '/api/getMusic',
        data: info_send,
        dataType: 'json',   // The type of data that you're expecting back from the server.
        //contentType: 'application/json; charset=utf-8', // Used 'application/json' only when is NOT GETing data with query string.
        success: function (data) {
            // TODO This call is made to a not yet created Player object.
            //Player.pause();

            // Get the music path if locally (not used any more), or a Youtube video ID.
            //document.getElementById("audiosrc").src=data.musicPath;
            // TODO modify the send source from AUDIO to the DIV data-src??? (NEEDS to call datachange event!)
            var player = $('#player');
            var params = {
                sourceType: 'youtube',  // TODO, read from server.
                source: data.musicPath,
                infoAlbumArt: data.imagePath,   // Currently not used.
                infoAlbumTitle: data.Album,
                infoArtist: data.Artist,
                infoTitle: data.Titre,
                infoLabel: data.Label,
                infoYear: data.Annee
            };
            player.trigger('loadNew', params);


            //ytPlayer.loadVideoById(data.musicPath, 5, "small");
            //console.log(ytPlayer);

            //Player = document.getElementById("Player");
            //Player.setAttribute('data-info-Title', data.Titre);
            //Player.setAttribute('data-info-Album-Title', data.Album);
            //Player.setAttribute('data-info-Artist', data.Artist);
            //Player.setAttribute('data-info-Label', data.Label);
            //Player.setAttribute('data-info-Year', data.Annee);
            //Player.setAttribute('data-info-Album-Art', data.imagePath);
            //document.getElementsByClassName("thumbnail")[0].src = data.imagePath;
            //
            //tableau = document.getElementsByClassName("table table-condensed")[0];
            //elements = tableau.getElementsByTagName('td');
            //elements[0].innerHTML = data.Artist;
            //elements[1].innerHTML = data.Titre;
            //elements[2].innerHTML = data.Album;
            //elements[3].innerHTML = data.Label;
            //elements[4].innerHTML = data.Annee;
            //Player.load();
            //Player.play();

        },
        error: function (data) {
            console.log("Error:");
            console.log(data);
        }
    });
}