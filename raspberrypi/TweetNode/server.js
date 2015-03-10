var express = require('express')
  , app = express()
  , http = require('http')
  , server = http.createServer(app)
  , Twit = require('twit')
  , io = require('socket.io').listen(server);
server.listen(4040);

// routing
// Tell node to load node-twitter-stream.html when the browser requests /
app.get('/', function (req, res) {
  res.sendFile(__dirname + '/node-twitter-stream.html');
});

// Tell node to serve the CSS file when requested
app.get('/node-twitter-stream.css', function (req, res) {
  res.sendFile(__dirname + '/node-twitter-stream.css');
});

// When processing the Twitter firehose, only show Tweets with these keywords
var watchList = ['@thinkingjuice,@weareemerge,@sephallen,@tjxmaspi,@ben_poulson,@dj10dj100'];

var T = new Twit({
consumer_key:             ''
  , consumer_secret:      ''
  , access_token:         ''
  , access_token_secret:  ''
});

io.sockets.on('connection', function (socket) {
  var stream = T.stream('statuses/filter', { track: watchList })
  //var stream = T.stream('statuses/sample') // Firehose (sampling of all Tweets)
  //var stream = T.stream('user') // Your user stream

  // When a Tweet is recieved:
  stream.on('tweet', function (tweet) {
    // Makes a link the Tweet clickable
    var turl = tweet.text.match( /(http|https|ftp):\/\/[^\s]*/i )
    if ( turl != null ) {
      turl = tweet.text.replace( turl[0], '<a href="'+turl[0]+'" target="new">'+turl[0]+'</a>' );
    } else {
      turl = tweet.text;
    }
    var mediaUrl;
    // Does the Tweet have an image attached?
    if ( tweet.entities['media'] ) {
      if ( tweet.entities['media'][0].type == "photo" ) {
        mediaUrl = tweet.entities['media'][0].media_url;
      } else {
        mediaUrl = null;
      }
    }
    // Does the Tweet contain the #littledonkey hashtag?
    var littleDonkey = turl.match(/littledonkey/gi)
    if ( littleDonkey != null ) {
      mediaUrl = 'http://share.gifyoutube.com/ZRMz66.gif'
    }
    // Does the Tweet contain the #jinglebells hashtag?
    var jingleBells = turl.match(/jinglebells/gi)
    if ( jingleBells != null ) {
      mediaUrl = 'http://share.gifyoutube.com/aeD0B8.gif'
    }
    var jingleBells = turl.match(/webcam/gi)
    if ( jingleBells != null ) {
      mediaUrl = 'http://christmaspi:8081/'
    }
    var youTube = turl.match(/#cheese/gi)
    if ( youTube != null ) {

      turl = turl.concat( '<div class="youtube"><iframe src="//www.youtube.com/embed/M2dhD9zR6hk?autoplay=1" frameborder="0"></iframe></div>' );
    }
    // Does the Tweet contain a valid YouTube ID?
    var youTube = turl.match(/#yt-/gi)
    if ( youTube != null ) {
      var str = turl;
      var regex = /#yt-([a-zA-Z0-9_-]{1,11})/gi;
      var matches = str.match(regex);
      var ytid = matches[0].replace("#yt-", "");
      turl = turl.concat( '<div class="youtube"><iframe src="//www.youtube.com/embed/'+ytid+'?autoplay=1" frameborder="0"></iframe></div>' );
    }
    // Does the Tweet contain a valid Vimeo ID?
    var vimeo = turl.match(/#vm-/gi)
    if ( vimeo != null ) {
      var str = turl;
      var regex = /#vm-([0-9]{1,11})/gi;
      var matches = str.match(regex);
      var vmid = matches[0].replace("#vm-", "");
      turl = turl.concat( '<div class="youtube"><iframe src="//player.vimeo.com/video/'+vmid+'?autoplay=1" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div>' );
    }
    // Does the Tweet contain a valid SoundCloud ID?
    var soundCloud = turl.match(/#sc-/gi)
    if ( soundCloud != null ) {
      var str = turl;
      var regex = /#sc-([a-zA-Z0-9]{1,11})/gi;
      var matches = str.match(regex);
      var scid = matches[0].replace("#sc-", "");
      turl = turl.concat( '<div class="youtube"><iframe scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/'+scid+'&amp;auto_play=true&amp;hide_related=true&amp;show_comments=true&amp;show_user=true&amp;show_reposts=false&amp;visual=true"></iframe></div>' );
    }
    // Send the Tweet to the browser
    io.sockets.emit('stream',turl, tweet.user.screen_name, tweet.user.profile_image_url, mediaUrl);
  });
});
