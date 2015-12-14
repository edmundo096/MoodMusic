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
            var player = $('#player');
            var params = {
                sourceType: 'youtube',  // TODO, read from server.
                source: data.music_path,
                infoAlbumArt: data.image_path,   // Currently not used.
                infoAlbumTitle: data.album,
                infoArtist: data.artist,
                infoTitle: data.title,
                infoLabel: data.label,
                infoYear: data.year
            };
            player.trigger('loadNew', params);

            // Reset rating stars color.
            $('#rating-1').css('color', '#aaa');
            $('#rating-2').css('color', '#aaa');
            $('#rating-3').css('color', '#aaa');
            $('#rating-4').css('color', '#aaa');
            $('#rating-5').css('color', '#aaa');
            // Reset mood combo text.
            document.getElementById("comboselect").options[0].text = 'Choose a mood';
        },
        error: function (data) {
            console.log("Error:");
            console.log(data);
        }
    });
}