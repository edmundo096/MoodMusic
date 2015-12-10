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
    jqButtonToggle.click(function () { jqSectionData.collapse('toggle'); });
    jqButtonToggle.tooltip({'container': 'body', 'placement': 'top', 'html': true});

    // Set up player event for loading new videos.
    jqPlayer.on('loadNew', function(event, params) {
        // If no parameters, exit.
        if (!params) { console.log('Player: Emtpy parameters.'); return; }

        reloadData(params);
    });

    // Set initial information data load.
    initialLoadData();


    var load_error = function () {
        // console.log('error');
        jqPlayer.find('.btn').addClass('disabled');
        jqPlayer.find('input[type="range"]').hide();
        jqPlayer.find('.glyphicon-refresh').text('Error');
        jqPlayer.find('.glyphicon-refresh').parent().attr('title', 'There was an error loading the audio.');
        jqPlayer.find('.glyphicon-refresh').parent().tooltip('fixTitle');
        jqPlayer.find('.glyphicon-refresh').removeClass('glyphicon glyphicon-refresh spin');
    }; // load_error


    // Function to update the Time from YT.
    var updateTimeFromYT = function() {
        var percentageLoaded = ytPlayer.getVideoLoadedFraction();
        var currentTime = ytPlayer.getCurrentTime();
        var duration = ytPlayer.getDuration();

        // Create a simulated TimeRanges Object with only 1 range.
        //srcTag.buffered = {
        //    length: 1,
        //    start: function(i) { return 0; },
        //    end: function(i) { return duration * percentageLoaded; }
        //};
        //srcTag.currentTime = currentTime;
        //srcTag.duration = duration;
        //srcTag.paused = ytPlayer.getPlayerState() != YT.PlayerState.PLAYING;
        //srcTag.networkState = 0;
        //srcTag.readyState = 0;  // Only used 1 time at setup.
        //srcTag.loop = 0;
        //srcTag.muted = ytPlayer.isMuted();
        //srcTag.volume = ytPlayer.getVolume()/100;

        jqSliderTime.val(currentTime);
        jqButtonCurrentTimeReset.text(currentTime);
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

            // Else, modify DOM.
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
    }

    function onPlayerError(event) {
        console.error('Player: Error on YT player. ERR code: ' + event.data +
            '.\nSee more at: https://developers.google.com/youtube/iframe_api_reference#Events');
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
            console.log('Player: Parameter sourceType is not "youtube", parameters:');
            console.log(paramsObj);
            return;
        }

        console.log('Player: Reloading data with:');
        console.log(paramsObj);
        // Update data attributes (just as reference!).
        jqPlayer.data('sourceType', paramsObj.sourceType);
        jqPlayer.data('source', paramsObj.source);

        jqPlayer.data('infoAlbumArt', paramsObj.infoAlbumArt);      // Currently not used.
        jqPlayer.data('infoAlbumTitle', paramsObj.infoAlbumTitle);
        jqPlayer.data('infoArtist', paramsObj.infoArtist);
        jqPlayer.data('infoTitle', paramsObj.infoTitle);
        jqPlayer.data('infoLabel', paramsObj.infoLabel);
        jqPlayer.data('infoYear', paramsObj.infoYear);

        // Load YT video.
        window.ytPlayer.loadVideoById(paramsObj.source);

        // Update Information data.
        $('#row-artist').find('td').first().text(paramsObj.infoArtist);
        $('#row-title').find('td').first().text(paramsObj.infoTitle);
        $('#row-album').find('td').first().text(paramsObj.infoAlbumTitle);
        $('#row-label').find('td').first().text(paramsObj.infoLabel);
        $('#row-year').find('td').first().text(paramsObj.infoYear);
    }




    $('audio[controls]').before(function () {

        var song = this;
        song.controls = false;

        var player_box = document.createElement('div');
        $(player_box).addClass($(song).attr('class') + ' well container-fluid playa');

        var data_sec = document.createElement('section');
        $(data_sec).addClass('collapsing center-block row col-sm-12');

        var toggle_holder = document.createElement('div');
        $(toggle_holder).addClass('btn-group center-block row col-sm-12');

        var data_toggle = document.createElement('button');
        $(data_toggle).html('<i class="glyphicon glyphicon-align-justify" style="top:-3px"></i>');
        $(data_toggle).addClass('btn btn-default btn-lg btn-block row col-sm-12');
        $(data_toggle).attr('style', 'opacity:0.3');
        $(data_toggle).click(function () {$(data_sec).collapse('toggle'); });
        $(data_toggle).attr('title', 'Details');
        $(data_toggle).tooltip({'container': 'body', 'placement': 'top', 'html': true});
        $(toggle_holder).append(data_toggle);

        var data_table = document.createElement('table');
        $(data_table).addClass('table table-condensed');

        var player = document.createElement('section');
        $(player).addClass('btn-group  center-block row  col-sm-12');




        //var load_error = function () {
        //    // console.log('error');
        //    jqPlayer.find('.btn').addClass('disabled');
        //    jqPlayer.find('input[type="range"]').hide();
        //    jqPlayer.find('.glyphicon-refresh').text('Error');
        //    jqPlayer.find('.glyphicon-refresh').parent().attr('title', 'There was an error loading the audio.');
        //    jqPlayer.find('.glyphicon-refresh').parent().tooltip('fixTitle');
        //    jqPlayer.find('.glyphicon-refresh').removeClass('glyphicon glyphicon-refresh spin');
        //}; // load_error



        var addPlay = function () {
            var play = document.createElement('button');
            $(play).addClass('btn  btn-default disabled col-sm-1');

            play.setPlayState = function (toggle) {
                $(play).removeClass('disabled');
                if (toggle === 'play') {
                    $(play).html('<i class="glyphicon glyphicon-play"></i>');
                    $(play).click(function () {
                        song.play();
                    });
                }
                if (toggle === 'pause') {
                    $(play).html('<i class="glyphicon glyphicon-pause"></i>');
                    $(play).click(function () {
                        song.pause();
                    });
                }
            }; // setPlayState

            // media events from the audio element will trigger rebuilding the play button
            $(song).on('play', function () {play.setPlayState('pause'); });
            $(song).on('canplay', function () {play.setPlayState('play'); });
            $(song).on('pause', function () {play.setPlayState('play'); });

            var timeout = 0;

            var loadCheck = setInterval(function () {
                if (isNaN(song.duration) === false) {
                    play.setPlayState('play');
                    clearInterval(loadCheck);
                    return true;
                }
                //if (song.networkState === 3 || timeout === 100) {
                //    // 3 = NETWORK_NO_SOURCE - no audio/video source found
                //    console.log('No audio source was found or a timeout occurred');
                //    load_error();
                //    clearInterval(loadCheck);
                //    return false;
                //}
                timeout++;
            }, 100); // x milliseconds per attempt
            $(player).append(play);
        }; // addPlay

        var addSeek = function () {
            var seek = document.createElement('input');
            $(seek).attr({
                'type': 'range',
                'min': 0,
                'value': 0,
                'class': 'seek'
            });

            seek.progress = function () {
                var i, bufferedstart, bufferedend;
                var bg = 'rgba(223, 240, 216, 1) 0%';
                bg += ', rgba(223, 240, 216, 1) ' + ((song.currentTime / song.duration) * 100) + '%';
                bg += ', rgba(223, 240, 216, 0) ' + ((song.currentTime / song.duration) * 100) + '%';
                for (i = 0; i < song.buffered.length; i++) {
                    if (song.buffered.end(i) > song.currentTime && 
                        isNaN(song.buffered.end(i)) === false && 
                        isNaN(song.buffered.start(i)) === false) {
                        
                        if (song.buffered.end(i) < song.duration) {
                            bufferedend = ((song.buffered.end(i) / song.duration) * 100);
                        } else {
                            bufferedend = 100;
                        }
                        if (song.buffered.start(i) > song.currentTime) {
                            bufferedstart = ((song.buffered.start(i) / song.duration) * 100);
                        } else {
                            bufferedstart = ((song.currentTime / song.duration) * 100);
                        }
                        bg += ', rgba(217, 237, 247, 0) ' + bufferedstart + '%';
                        bg += ', rgba(217, 237, 247, 1) ' + bufferedstart + '%';
                        bg += ', rgba(217, 237, 247, 1) ' + bufferedend + '%';
                        bg += ', rgba(217, 237, 247, 0) ' + bufferedend + '%';
                    }
                }
                $(seek).css('background', '-webkit-linear-gradient(left, ' + bg + ')');
                    //These may be re-enabled when/if other browsers support the background like webkit
                    //$(seek).css('background','-o-linear-gradient(left,  ' + bg + ')');
                    //$(seek).css('background','-moz-linear-gradient(left,  ' + bg + ')');
                    //$(seek).css('background','-ms-linear-gradient(left,  ' + bg + ')');
                    //$(seek).css('background','linear-gradient(to right,  ' + bg + ')');
                $(seek).css('background-color', '#ddd');
            }; // seek.progress

            seek.set = function () {
                $(seek).val(song.currentTime);
                seek.progress();
            };

            seek.slide = function () {
                song.currentTime = $(seek).val();
                seek.progress();
            };

            seek.init = function () {
                $(seek).attr({
                    'max': song.duration,
                    'step': song.duration / 100
                });
                seek.set();
            };

            seek.reset = function () {
                $(seek).val(0);
                song.currentTime = $(seek).val();
                if (!song.loop) {
                    song.pause();
                } else {
                    song.play();
                }
            };

            var seek_wrapper = document.createElement('div');
            $(seek_wrapper).addClass('btn btn-default col-sm-4 hidden-xs');
            $(seek_wrapper).append(seek);

            // bind seek / position slider events
            $(seek).on('change', seek.slide);

            // bind audio element events to trigger seek slider updates
            $(song).on('timeupdate', seek.init);
            $(song).on('loadedmetadata', seek.init);
            $(song).on('loadeddata', seek.init);
            $(song).on('progress', seek.init);
            $(song).on('canplay', seek.init);
            $(song).on('canplaythrough', seek.init);
            $(song).on('ended', seek.reset);
            if (song.readyState > 0) {
                seek.init();
            }

            $(player).append(seek_wrapper);
        }; // addSeek

        var addTime = function () {
            var time = document.createElement('button');
            $(time).addClass('btn btn-default col-sm-3');
            $(time).tooltip({'container': 'body', 'placement': 'right', 'html': true});

            time.twodigit = function (myNum) {
                return ('0' + myNum).slice(-2);
            }; // time.twodigit

            time.timesplit = function (a) {
                if (isNaN(a)) {
                    return '<i class="glyphicon glyphicon-refresh spin"></i>';
                }
                var hours = Math.floor(a / 3600);
                var minutes = Math.floor(a / 60) - (hours * 60);
                var seconds = Math.floor(a) - (hours * 3600) - (minutes * 60);
                var timeStr = time.twodigit(minutes) + ':' + time.twodigit(seconds);
                if (hours > 0) {
                    timeStr = hours + ':' + timeStr;
                }
                return timeStr;
            }; // time.timesplit

            time.showtime = function () {
                var position_title = 'Click to Reset<hr style="padding:0; margin:0;" />Position: ';
                var length_title = 'Click to Reset<hr style="padding:0; margin:0;" />Length: ';
                if (!song.paused) {
                    $(time).html(time.timesplit(song.currentTime));
                    $(time).attr({'title': length_title + (time.timesplit(song.duration))});
                } else {
                    $(time).html(time.timesplit(song.duration));
                    $(time).attr({'title': position_title  + (time.timesplit(song.currentTime))});
                }
                $(time).tooltip('fixTitle');
            }; // time.showtime

            $(time).click(function () {
                song.pause();
                song.currentTime = 0;
                time.showtime();
                $(time).tooltip('fixTitle');
                $(time).tooltip('show');
            }); // time.click

            $(time).tooltip('show');
            $(song).on('loadedmetadata', time.showtime);
            $(song).on('loadeddata', time.showtime);
            $(song).on('progress', time.showtime);
            $(song).on('canplay', time.showtime);
            $(song).on('canplaythrough', time.showtime);
            $(song).on('timeupdate', time.showtime);
            if (song.readyState > 0) {
                time.showtime();
            } else {
                $(time).html('<i class="glyphicon glyphicon-refresh spin"></i>');
            }
            $(player).append(time);
        }; // addTime

        var addMute = function () {
            var mute = document.createElement('button');
            $(mute).addClass('btn btn-default  col-sm-1');

            mute.checkVolume = function () {
                if (song.volume > 0.5 && !song.muted) {
                    $(mute).html('<i class="glyphicon glyphicon-volume-up"></i>');
                } else if (song.volume < 0.5 && song.volume > 0 && !song.muted) {
                    $(mute).html('<i class="glyphicon glyphicon-volume-down"></i>');
                } else {
                    $(mute).html('<i class="glyphicon glyphicon-volume-off"></i>');
                }
            }; // mute.checkVolume

            $(mute).click( function () {
                if (song.muted) {
                    song.muted = false;
                    song.volume = song.oldvolume;
                } else {
                    song.muted = true;
                    song.oldvolume = song.volume;
                    song.volume = 0;
                }
                mute.checkVolume();
            }); // mute.click(

            mute.checkVolume();
            $(song).on('volumechange', mute.checkVolume);
            $(player).append(mute);
        }; // addMute

        var addVolume = function () {
            var volume = document.createElement('input');
            $(volume).attr({
                'type': 'range',
                'min': 0,
                'max': 1,
                'step': 1 / 100,
                'value': 1
            });

            volume.slide = function () {
                song.muted = false;
                song.volume = $(volume).val();
            }; // volume.slide

            volume.set = function () {
                $(volume).val(song.volume);
            };

            var vol_wrapper = document.createElement('div');
            $(vol_wrapper).addClass('btn  btn-default  row col-sm-3  hidden-xs');
            $(vol_wrapper).append(volume);
            $(volume).on('change', volume.slide);
            $(song).on('volumechange', volume.set);
            $(player).append(vol_wrapper);

        }; // addVolume

        var addAlbumArt = function () {
            var albumArt = document.createElement('img');
            $(albumArt).addClass('thumbnail');
            $(albumArt).attr('src', $(song).data('infoAlbumArt'));
            $(data_sec).append(albumArt);
        }; // addAlbumArt

        var addInfo = function (title, dataId) {
            var row = document.createElement('tr');
            var head = document.createElement('th');
            var data = document.createElement('td');
            $(head).html(title);
            $(data).html($(song).data(dataId));
            $(row).append(head);
            $(row).append(data);
            $(data_table).append(row);
        }; // addInfo

        var addData = function () {
            // jslint will complain about our use of `typeof` but 
            // it's the only way not to raise an error by referencing 
            // a nnon-existent data-* variable 
            if (typeof ($(song).data('infoAlbumArt')) !== 'undefined') {
                addAlbumArt();
            }
            if (typeof ($(song).data('infoArtist')) !== 'undefined') {
                addInfo('Artist', 'infoArtist');
            }
            if (typeof ($(song).data('infoTitle')) !== 'undefined') {
                addInfo('Title', 'infoTitle');
            }
            if (typeof ($(song).data('infoAlbumTitle')) !== 'undefined') {
                addInfo('Album', 'infoAlbumTitle');
            }
            if (typeof ($(song).data('infoLabel')) !== 'undefined') {
                addInfo('Label', 'infoLabel');
            }
            if (typeof ($(song).data('infoYear')) !== 'undefined') {
                addInfo('Year', 'infoYear');
            }
            if ($(data_table).html() !== '') {
                $(data_sec).append(data_table);
                $(player_box).append(toggle_holder);
                $(player_box).append(data_sec);
            }
        }; // addData

        var addPlayer = function () {
            if ($(song).data('play') !== 'off') {
                addPlay();
            }
            if ($(song).data('seek') !== 'off') {
                addSeek();
            }
            if ($(song).data('time') !== 'off') {
                addTime();
            }
            if ($(song).data('mute') !== 'off') {
                addMute();
            }
            if ($(song).data('volume') !== 'off') {
                addVolume();
            }
            $(player_box).append(player);
        }; // addPlayer

        var addAttribution = function () {
            var attribution = document.createElement('div');
            $(attribution).addClass('row col-sm-10 col-sm-offset-1');
            if (typeof ($(song).data('infoAttLink')) !== 'undefined') {
                var attribution_link = document.createElement('a');
                $(attribution_link).addClass('text-muted btn btn-link btn-sm');
                $(attribution_link).attr('href', $(song).data('infoAttLink'));
                $(attribution_link).html($(song).data('infoAtt'));
                $(attribution).append(attribution_link);
            } else {
                $(attribution).html($(song).data('infoAtt'));
            }
            $(player_box).append(attribution);
        }; // addAttribution

        var fillPlayerBox = function () {
            addData();
            addPlayer();
            if (typeof ($(song).data('infoAtt')) !== 'undefined') {
                addAttribution();
            }
        }; // fillPlayerBox

        fillPlayerBox();
        $(song).on('error', function () {
            console.log("Error encountered after fillPlayerBox");
            load_error();
        });
        return player_box;
    });
})(jQuery);
