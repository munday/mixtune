var currentTrack = -1;
var progressInterval;
var songs = {};

function getAudio(){
    var a = document.getElementById('audio');

    var spot = document.getElementById('player_container');

    if(!a){
        a = document.createElement('audio');
        a.id = 'audio';
	spot.appendChild(a);
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

function playMp3(path,num){

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
            console.log(msg);
            drawPlaylist(msg);
        });    

}

function drawPlaylist(s){

    songs = s;
    var color = 0x0b0;
    var dx = 1;

    //document.body.innerHTML = '';

    var table = document.getElementById('songlist');
    var tbody = table.getElementsByTagName('tbody')[0];
    
    tbody.innerHTML = '';

    for(x=0;x<s.length;x++){

	var tr = document.createElement('tr');
        var tdControls = document.createElement('td');
        var tdTitle = document.createElement('td');
        var tdArtist = document.createElement('td');
        var tdSource = document.createElement('td');

	tr.id='track'+x;

        
	tdControls.innerHTML = '<div id="play_pause'+x+'" class="icon-play"></div>';
	tdControls.onclick= function(){
		var d = this.data.split(':'); 
                playMp3(d[0],d[1]); 
	}
        tdControls.data = s[x].local_url + ':' + x;

        tdTitle.innerHTML = s[x].id3_title;
	tdArtist.innerHTML = s[x].id3_artist;

        tr.appendChild(tdControls);
        tr.appendChild(tdTitle);
        tr.appendChild(tdArtist);
        tr.appendChild(tdSource);

	table.appendChild(tr);

    }

}



function getAlbumArt(title){
    var script = document.createElement('script');
    script.src = 'http://api.discogs.com/artists/1?callback=changeBg';
}

function nextTrack(){
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
	progress.style.width = pct + '%';	
}

function clearAllProgress(){
	for(x=0;x<songs.length;x++){
		setProgress(x,0);
	}
}
