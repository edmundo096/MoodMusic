var ytPlayer;

function getMusic(item) {
    var info_send = {
        'music': item.target.innerHTML.split("> ")[1].substring(0, item.target.innerHTML.split("> ")[1].length - 1)
    };

    console.log(item.target.innerHTML.split("> ")[1].substring(0, item.target.innerHTML.split("> ")[1].length - 1));

    $.ajax({
        type: 'POST',
        url: '/api/getMusic',
        data: JSON.stringify(info_send),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            Player.pause();

            // Get the music path if locally (not used any more), or a Youtube video ID.
            //document.getElementById("audiosrc").src=data.musicPath;
            ytPlayer.loadVideoById(data.musicPath, 5, "small");
            console.log(ytPlayer);

            Player = document.getElementById("Player");
            Player.setAttribute('data-info-Title', data.Titre);
            Player.setAttribute('data-info-Album-Title', data.Album);
            Player.setAttribute('data-info-Artist', data.Artist);
            Player.setAttribute('data-info-Label', data.Label);
            Player.setAttribute('data-info-Year', data.Annee);
            Player.setAttribute('data-info-Album-Art', data.imagePath);
            document.getElementsByClassName("thumbnail")[0].src = data.imagePath;

            tableau = document.getElementsByClassName("table table-condensed")[0];
            elements = tableau.getElementsByTagName('td');
            elements[0].innerHTML = data.Artist;
            elements[1].innerHTML = data.Titre;
            elements[2].innerHTML = data.Album;
            elements[3].innerHTML = data.Label;
            elements[4].innerHTML = data.Annee;
            Player.load();
            Player.play();

        },
        error: function (data) {
            console.log("erreur");
        }
    });
}


// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.

function onYouTubeIframeAPIReady() {
    ytPlayer = new YT.Player('yt-player', {
        height: '390',
        width: '640',
        videoId: 'M7lc1UVf-VE',
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
//var done = false;
function onPlayerStateChange(event) {
    if (event.data == YT.PlayerState.PLAYING && !done) {
        //setTimeout(stopVideo, 6000);
        //done = true;
    }
}
//function stopVideo() {
//    ytPlayer.stopVideo();
//}
