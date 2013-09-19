var currentTrack = -1;
var progressInterval;
var songs = {};

function getAudio(){
    var a = document.getElementById('audio');
    if(!a){
        a = document.createElement('audio');
        a.id = 'audio';
	document.body.appendChild(a);
    }
    
    a.addEventListener('ended', nextTrack);
   
    return a;
}

function canPlayAudio(audio, type){

    var t = 'audio/mpeg';

    switch(type){
        case 2:
            type='audio/ogg; codecs="vorbis"';
        break;	
    }
        
    if (audio.canPlayType) {
       // Currently canPlayType(type) returns: "", "maybe" or "probably" 
       return !!audio.canPlayType && "" != audio.canPlayType(t);
    }

    return false;

}


function playMp3_orig(path,num){

    var audio = getAudio();
    $('.track').each(function(a,itm){$('#track'+a).removeClass('selected')});
    $('#track'+num).addClass('selected');
    if(canPlayAudio(audio,1)){
        audio.src = path;
	audio.controls = true;
        audio.play();
	currentTrack=num;
	clearInterval(progressInterval);
	clearAllProgress();
	progressInterval = setInterval(updateProgress,200);
    }
	
}

function playMp3(path,num){

    soundManager.stopAll();
    clearAllProgress();
    currentTrack = num;

    $('.track').each(function(a,itm){$('#track'+a).removeClass('selected')});
    $('#track'+num).addClass('selected');

    var soundId = 'track' + num;
    var sound = soundManager.createSound({id: soundId, url: path, whileplaying: function(){progress(this.position, this.duration)} });
    sound.play();
	
}

function progress(time, duration) {
    setProgress(currentTrack, time/duration * 100);
}

function getPlaylist(d){

    var day = d.getDate();
    var month = d.getMonth()+1;
    var year = d.getFullYear();

    if(day<10){
        day = '0'+day;	
    }

    if(month<10){
        month = '0'+month;	
    }


    $.ajax({
        type: "GET",
        url: "http://hacks.so/playlists/songs-"+year+"-"+month+"-"+day+".json",
        data: {},
	statusCode: {
            404: function() {
                var nd = new Date(year,month-1,day-1);
                getPlaylist(nd);
            }
  	}
    }).done(function( msg ) {
        drawPlaylist(msg);
    });    

}

function drawPlaylist(s){

    songs = s;
    var color = 0x0b0;
    var dx = 1;

    var wrap = document.getElementById('wrap');
    wrap.innerHTML = '<div id="sticky" class="gone track"></div>';
    
    for(x=0;x<s.length;x++){

        var div = document.createElement('div');
        
        if(color==0x0f0){
            dx = -1;
        }else if(color==0x0b0){
            dx = 1;
        }

        div.id = 'track' + x;
        div.setAttribute('class','track ' + color.toString(16));
        div.onclick = function(){
            var d = this.data.split(':'); 
            clearCurrent();
            playMp3(d[0],d[1]); 
        };
        div.data = s[x].local_url + ':' + x;
        div.innerHTML = /*'<span>&#9734;</span>&nbsp;*/ '<span class="title">' + s[x].id3_title + '</span><span class="dash">-</span><span class="artist">' + s[x].id3_artist + '</span><div class="progress" id="progress'+x+'"></div>';
        wrap.appendChild(div);
        color+=16*dx;
    }

    $(window).scroll(stickCurrent);

}

function getAlbumArt(title){
    var script = document.createElement('script');
    script.src = 'http://api.discogs.com/artists/1?callback=changeBg';
}

function nextTrack(){
    clearCurrent();
    currentTrack++;
    var itm = document.getElementById('track'+currentTrack);
    if(itm){
        var path = itm.data.split(':')[0];
        playMp3(path,currentTrack);
    }else{
        currentTrack=-1;
        nextTrack();
    }

}

function updateProgress(){
    var audio = document.getElementById('audio');
    setProgress(currentTrack, audio.currentTime/audio.duration * 100);
}

function setProgress(num,pct){
    var progress = document.getElementById('track'+num).getElementsByClassName('progress')[0];
    var progress2 = document.getElementById('sticky').getElementsByClassName('progress')[0];
    if (progress) progress.style.width = pct + '%';
    if (progress2) progress2.style.width = pct + '%';
}

function clearAllProgress(){
    for(x=0;x<songs.length;x++){
        setProgress(x,0);
    }
}

function clearCurrent() {
    sticky=$('#sticky');
    sticky.addClass('gone');
    sticky.removeClass('sticky_top');
    sticky.removeClass('sticky_bottom');	
}

function stickCurrent() {
    var div = $('.selected');
    var sticky = $('#sticky');

    sticky.html(div.html());    

    var offset = div.offset()?div.offset().top:top;
    var top = $(window).scrollTop();

    var height = $(window).height();
    var nextOffset = div.next().offset()?div.next().offset().top:top+height;

    if (top > offset) {
	sticky.removeClass('gone');
	sticky.addClass('sticky_top');
	sticky.removeClass('sticky_bottom');
    } else if( top+height < nextOffset ) {
	sticky.removeClass('gone');
	sticky.addClass('sticky_bottom');
	sticky.removeClass('sticky_top');
    } else  {
        sticky.addClass('gone');
	sticky.removeClass('sticky_top');
	sticky.removeClass('sticky_bottom');
    }

}
