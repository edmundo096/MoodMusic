function setRating(item) {

    var player = $('#player');

    var rat1 = $('#rating-1');
    var rat2 = $('#rating-2');
    var rat3 = $('#rating-3');
    var rat4 = $('#rating-4');
    var rat5 = $('#rating-5');

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
            console.log("setRating success");

            // Use the server result to color the starts.
            var ratSet = data.success;

            ratSet >= 1 ? rat1.css('color', 'orange') : rat1.css('color', '#aaa');
            ratSet >= 2 ? rat2.css('color', 'orange') : rat2.css('color', '#aaa');
            ratSet >= 3 ? rat3.css('color', 'orange') : rat3.css('color', '#aaa');
            ratSet >= 4 ? rat4.css('color', 'orange') : rat4.css('color', '#aaa');
            ratSet == 5 ? rat5.css('color', 'orange') : rat5.css('color', '#aaa');
        },
        error: function (data) {
            console.log("setRating error");
        }
    });
}


["#rating-5", "#rating-4", "#rating-3", "#rating-2", "#rating-1"].forEach(function (item) {
    $(item).on("click", function (event) {
        setRating($(item));
    });
});
