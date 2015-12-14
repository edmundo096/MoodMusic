function setRating(item) {

    var player = $('#player');

    var info_sent = {
        rating: item['selector'].split('-')[1],
        artist: player.attr('data-info-artist'),
        album: player.attr('data-info-album-title'),
        title: player.attr('data-info-title')
    };

    console.log(info_sent);

    $.ajax({
        type: 'POST',
        url: '/api/rating',
        data: JSON.stringify(info_sent),
        dataType: 'json',
        contentType: 'application/json; charset=utf-8',
        success: function (data) {
            console.log("setRating success")
        },
        error: function (data) {
            console.log("setRating error")
        }
    });
}


["#rating-5", "#rating-4", "#rating-3", "#rating-2", "#rating-1"].forEach(function (item) {
    $(item).on("click", function (event) {
        setRating($(item));
    });
});
