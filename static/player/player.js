/* global jQuery */
(function ($) {
    'use strict';

    var jqPlayer                = $('#player');

    var jqButtonToggle          = $('#button-toggle');
    var jqSectionData           = $('#section-data');

    var jqSectionPlayerControls = $('#section-player-controls');
    var jqButtonPlayPause       = $('#button-play-pause');
    var jqSliderTime            = $('#sider-time');
    var jqButtonCurrentTimeReset= $('#button-current-time-reset');
    var jqButtonMute            = $('#button-mute');
    var jqSliderVolume          = $('#sider-volume');


    // Process YouTube Div to iFrame.
    // Save ytPlayer as window global variable.
    window.onYouTubeIframeAPIReady = function() {
        window.ytPlayer = new YT.Player('yt-player', {
            height: '390',
            width: '640',
            videoId: jqPlayer.data('source'),
            events: {
                'onReady': onPlayerReady,
                'onStateChange': onPlayerStateChange,
                'onError': onPlayerError
            },
            playerVars: {
                controls: 0
            }
        });
    };

    // Load the YouTube iFrame API script.
    $('script').first().before(function() {
        var tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        return tag;
    });

    // Set up buttons.
    jqButtonToggle.click(function() { jqSectionData.collapse('toggle'); });
    jqButtonToggle.tooltip({'container': 'body', 'placement': 'top', 'html': true});
    jqButtonCurrentTimeReset.tooltip({'container': 'body', 'placement': 'top', 'html': true});

    // Set up player event for loading new videos.
    jqPlayer.on('loadNew', function(event, params) {
        // If no parameters, exit.
        if (!params) { console.log('Player: Emtpy parameters.'); return; }

        reloadData(params);
    });

    // Set initial information data load.
    initialLoadData();


    // Closure Function to update the controls as active or inactive,
    var load_error = function() {
        var areDeactivated = false;
        return function(deactivateControls) {
            // console.log('error');
            if (deactivateControls && !areDeactivated) {
                jqPlayer.find('.btn').addClass('disabled');
                jqPlayer.find('input[type="range"]').hide();
                //jqPlayer.find('.glyphicon-refresh').text('Error');
                jqButtonCurrentTimeReset.text('Error');
                jqPlayer.find('.glyphicon-refresh').parent().attr('title', 'There was an error loading the audio.');
                //jqPlayer.find('.glyphicon-refresh').parent().tooltip('fixTitle');
                jqPlayer.find('.glyphicon-refresh').removeClass('glyphicon glyphicon-refresh spin');
                areDeactivated = true;
            }
            else if (!deactivateControls && areDeactivated) {
                // Reactivate.
                jqPlayer.find('.btn').removeClass('disabled');
                jqPlayer.find('input[type="range"]').show();
                jqButtonCurrentTimeReset.html('<i class="glyphicon glyphicon-refresh spin"></i>');
                jqButtonCurrentTimeReset.attr('title', 'Loading');
                areDeactivated = false;
            }
        };
    }(); // load_error


    // Function to update the Time from YT.
    var updateTimeFromYT = function() {
        var percentageLoaded = ytPlayer.getVideoLoadedFraction();
        var currentTime = ytPlayer.getCurrentTime();
        var duration = ytPlayer.getDuration();
        // Create a simulated TimeRanges Object with only 1 range.
        var buffered = {
            length: 1,
            start: function(i) { return 0; },
            end: function(i) { return duration * percentageLoaded; }
        };

        // Update controls.

        // Time Slider.
        jqSliderTime.val(currentTime);

        // Time Slider background.
        var timeBgUpdate = function () {
            var i, bufferedstart, bufferedend;
            var bg = 'rgba(223, 240, 216, 1) 0%';
            bg += ', rgba(223, 240, 216, 1) ' + ((currentTime / duration) * 100) + '%';
            bg += ', rgba(223, 240, 216, 0) ' + ((currentTime / duration) * 100) + '%';
            for (i = 0; i < buffered.length; i++) {
                if (buffered.end(i) > currentTime &&
                    isNaN(buffered.end(i)) === false &&
                    isNaN(buffered.start(i)) === false) {

                    if (buffered.end(i) < duration) {
                        bufferedend = ((buffered.end(i) / duration) * 100);
                    } else {
                        bufferedend = 100;
                    }
                    if (buffered.start(i) > currentTime) {
                        bufferedstart = ((buffered.start(i) / duration) * 100);
                    } else {
                        bufferedstart = ((currentTime / duration) * 100);
                    }
                    bg += ', rgba(217, 237, 247, 0) ' + bufferedstart + '%';
                    bg += ', rgba(217, 237, 247, 1) ' + bufferedstart + '%';
                    bg += ', rgba(217, 237, 247, 1) ' + bufferedend + '%';
                    bg += ', rgba(217, 237, 247, 0) ' + bufferedend + '%';
                }
            }
            jqSliderTime.css('background', '-webkit-linear-gradient(left, ' + bg + ')');
                //These may be re-enabled when/if other browsers support the background like webkit
                //$(seek).css('background','-o-linear-gradient(left,  ' + bg + ')');
                //$(seek).css('background','-moz-linear-gradient(left,  ' + bg + ')');
                //$(seek).css('background','-ms-linear-gradient(left,  ' + bg + ')');
                //$(seek).css('background','linear-gradient(to right,  ' + bg + ')');
            jqSliderTime.css('background-color', '#ddd');
        };
        timeBgUpdate();

        // Time and Reset button.
        var timesplit = function (a) {
            var twodigit = function (myNum) {
                return ('0' + myNum).slice(-2);
            };

            if (isNaN(a)) {
                return '<i class="glyphicon glyphicon-refresh spin"></i>';
            }
            var hours = Math.floor(a / 3600);
            var minutes = Math.floor(a / 60) - (hours * 60);
            var seconds = Math.floor(a) - (hours * 3600) - (minutes * 60);
            var timeStr = twodigit(minutes) + ':' + twodigit(seconds);
            if (hours > 0) {
                timeStr = hours + ':' + timeStr;
            }
            return timeStr;
        };
        var showtime = function () {
            var position_title = 'Click to Reset<hr style="padding:0; margin:0;" />Position: ';
            var length_title = 'Click to Reset<hr style="padding:0; margin:0;" />Length: ';
            if (ytPlayer.getPlayerState() !== YT.PlayerState.PAUSED) {
                jqButtonCurrentTimeReset.html(timesplit(currentTime));
                jqButtonCurrentTimeReset.attr({'title': length_title + (timesplit(duration))});
            } else {
                jqButtonCurrentTimeReset.html(timesplit(duration));
                jqButtonCurrentTimeReset.attr({'title': position_title  + (timesplit(currentTime))});
            }
            //jqButtonCurrentTimeReset.tooltip('fixTitle');
        };
        showtime();
    };
    // Closure Function to update the Volume and Mute controls, only if there are changes from YT since last update.
    var updateVolumeFromYT = function() {
        var previousVolume, wasMuted;
        return function() {
            var volume = ytPlayer.getVolume() / 100;
            var isMuted = ytPlayer.isMuted();

            // Exit if the previous values are still the same.
            if (volume === previousVolume && isMuted === wasMuted)
                return;

            // Else, set current values as previous, and modify DOM.
            previousVolume = volume;
            wasMuted = isMuted;

            if (volume > 0.5 && !isMuted) {
                jqButtonMute.html('<i class="glyphicon glyphicon-volume-up"></i>');
            } else if (volume < 0.5 && volume >= 0 && !isMuted) {
                jqButtonMute.html('<i class="glyphicon glyphicon-volume-down"></i>');
            } else {
                jqButtonMute.html('<i class="glyphicon glyphicon-volume-off"></i>');
            }
            jqSliderVolume.val(volume);
        };
    }();
    // Closure Function to turn On or Off the Time updating intervals.
    var updateTimeFromYTInterval = function() {
        var intervalId;
        return function(active) {
            // Clear last interval.
            window.clearInterval(intervalId);
            // Set a new interval if needed.
            if (active)
                intervalId = window.setInterval(updateTimeFromYT, 500);
        };
    }();
    // Closure Function to turn On or Off the Volume updating intervals.
    var updateVolumeFromYTInterval = function() {
        var intervalId;
        return function(active) {
            // Clear last interval.
            window.clearInterval(intervalId);
            // Set a new interval if needed.
            if (active)
                intervalId = window.setInterval(updateVolumeFromYT, 500);
        };
    }();


    function setPlayButtonStateAndTimeUpdatingInterval(isPlaying) {
        if (isPlaying) {
            jqButtonPlayPause.html('<i class="glyphicon glyphicon-pause"></i>');
            updateTimeFromYTInterval(true);
        }
        else {
            jqButtonPlayPause.html('<i class="glyphicon glyphicon-play"></i>');
            updateTimeFromYTInterval(false);
        }
    }


    function onPlayerReady(event) {
        var ytPlayer = event.target;

        // Initial controls update from YouTube player (except for play/pause, since is updated from stateChange).
        updateTimeFromYT();
        updateVolumeFromYT();
        // Start volume update interval.
        updateVolumeFromYTInterval(true);

        // Set controls attributes.......................................

        jqSliderTime.attr({
            'max': ytPlayer.getDuration(),
            'step': ytPlayer.getDuration() / 100
        });

        // Set events....................................................

        // Play/Pause
        jqButtonPlayPause.click(function(eventObject) {
            var state = ytPlayer.getPlayerState();

            if (state != YT.PlayerState.PLAYING) {
                ytPlayer.playVideo();
                setPlayButtonStateAndTimeUpdatingInterval(true);
            }
            else if (state != YT.PlayerState.PAUSED) {
                ytPlayer.pauseVideo();
                setPlayButtonStateAndTimeUpdatingInterval(false);
            }
        });

        // Time slider.
        jqSliderTime.mousedown(function(eventObject) {
            // Stop updating Time from YT.
            updateTimeFromYTInterval(false);
        });
        jqSliderTime.on('input', function(eventObject) {
            // Stop updating Time from YT (in case of no mouse), and seek without buffering.
            updateTimeFromYTInterval(false);
            ytPlayer.seekTo(eventObject.target.value, false);
        });
        jqSliderTime.change(function(eventObject) {
            // Resume updating Time from YT, and seek with buffering.
            updateTimeFromYTInterval(true);
            ytPlayer.seekTo(eventObject.target.value, true);
        });

        // Time reset.
        jqButtonCurrentTimeReset.click(function(eventObject) {
            ytPlayer.seekTo(0, true);
            // Update in case that the video is paused and the update interval is not active.
            updateTimeFromYT();
        });

        // Mute.
        jqButtonMute.click(function(eventObject) {
            ytPlayer.isMuted() ? ytPlayer.unMute() : ytPlayer.mute();
            updateVolumeFromYT();
        });

        // Volume slider.
        jqSliderVolume.mousedown(function(eventObject) {
            // Stop updating Volume from YT.
            updateVolumeFromYTInterval(false);
        });
        jqSliderVolume.on('input', function(eventObject) {
            // Stop updating Volume from YT (in case of no mouse), and change Volume.
            updateVolumeFromYTInterval(false);
            ytPlayer.setVolume(eventObject.target.value * 100);   // YT is 0 to 100.
        });
        jqSliderVolume.change(function(eventObject) {
            // Resume updating Volume from YT.
            updateVolumeFromYTInterval(true);
        });
    }

    function onPlayerStateChange(event) {
        console.log('Player: YT state: ' + event.data);

        // Update play/pause buttons states from YouTube.
        if (event.data == YT.PlayerState.PLAYING)
            setPlayButtonStateAndTimeUpdatingInterval(true);
        else if (event.data == YT.PlayerState.PAUSED)
            setPlayButtonStateAndTimeUpdatingInterval(false);


        // If loads a new video (plays it), Update controls attributes.
        //* Note that getDuration() will return 0 until the video's metadata is loaded, which normally happens just after the video starts playing.
        if (event.data == YT.PlayerState.PLAYING)
        jqSliderTime.attr({
            'max': event.target.getDuration(),
            'step': event.target.getDuration() / 100
        });
    }

    function onPlayerError(event) {
        console.error('Player: Error on YT player. ERR code: ' + event.data +
            '.\nSee more at: https://developers.google.com/youtube/iframe_api_reference#Events');

        load_error(true);
    }


    function initialLoadData() {
        // Update Information data.
        $('#row-artist').find('td').first().text(jqPlayer.data('infoArtist'));
        $('#row-title').find('td').first().text(jqPlayer.data('infoTitle'));
        $('#row-album').find('td').first().text(jqPlayer.data('infoAlbumTitle'));
        $('#row-label').find('td').first().text(jqPlayer.data('infoLabel'));
        $('#row-year').find('td').first().text(jqPlayer.data('infoYear'));
    }

    function reloadData(paramsObj) {
        // Check params and if source type is not youtube, then exit.
        if(paramsObj.sourceType !== 'youtube') {
            console.log('Player: Parameter sourceType is not "youtube", parameters...');
            console.log(paramsObj);
            return;
        }

        load_error(false);

        console.log('Player: Reloading data with...');
        console.log(paramsObj);
        // Update data attributes (just as reference!).
        jqPlayer.attr('data-source-type', paramsObj.sourceType);
        jqPlayer.attr('data-source', paramsObj.source);

        jqPlayer.attr('data-info-album-art', paramsObj.infoAlbumArt);      // Currently not used.
        jqPlayer.attr('data-info-album-title', paramsObj.infoAlbumTitle);
        jqPlayer.attr('data-info-artist', paramsObj.infoArtist);
        jqPlayer.attr('data-info-title', paramsObj.infoTitle);
        jqPlayer.attr('data-info-label', paramsObj.infoLabel);
        jqPlayer.attr('data-info-year', paramsObj.infoYear);

        // Load YT video.
        var ytPlayer = window.ytPlayer;
        ytPlayer.loadVideoById(paramsObj.source);

        // Update Information data.
        $('#row-artist').find('td').first().text(paramsObj.infoArtist);
        $('#row-title').find('td').first().text(paramsObj.infoTitle);
        $('#row-album').find('td').first().text(paramsObj.infoAlbumTitle);
        $('#row-label').find('td').first().text(paramsObj.infoLabel);
        $('#row-year').find('td').first().text(paramsObj.infoYear);
    }

})(jQuery);
