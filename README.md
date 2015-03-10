Interactive Christmas Tree
==========================

A project to make a Christmas tree interactive by proximity and Twitter for Thinking Juice.

Arduino
-------

This projects uses an Arduino to detect when a person's hands are close to the tree lights and then turn them on.
The final code for the Arduino can be found in the directory `arduino/IR_Proximity_Sensor_ClassInTab`.
This is an object orientated version of the original code to easily allow the addition of more LEDs, IR receivers and IR emitters.
The syntax for adding a new class instance (this needs to be put at the very top of your Arduino sketch) is:

`LEDProximity classinstancename(ledpin, irrecieverpin, iremitterpin, proximityvalue);`

Where `classinstancename` can be any name you wish to give this class instance.
`ledpin` is the pin number where the LED light is connected to the Arduino, eg: 3.
`irrecieverpin` is the pin number where the IR receiver is connected to the Arduino, this requires an analog pin, eg: A0.
`iremitterpin` is the pin number where the IR emitter LED is connected to the Arduino, eg: 2.
And finally `proximityvalue` is the value which you wish the LED lights will turn on, setting this to a low number will give a greater detection range, eg: 1.

###void setup()
In the `void setup()` block of the Ardunio sketch, we need to initialise the components plugged into the Arduino.
To do this we need to run the `setupProximity()` function for each class instance by typing `classinstancename.setupProximity();` where `classinstancename` is what we defined in the previous section. Each instance of the class needs to be initialised in the `void setup()` block individually, eg:

`classinstancename1.setupProximity();`

`classinstancename2.setupProximity();`

`classinstancename3.setupProximity();`

###void loop()
Finally, in the `void loop()` block of the sketch, we need to run the function `controlLED()` on each loop for the each class instance. The `controlLED()` function
calculates the ambient background infrared light to give us a working value in aiding us in detecting when an object is nearby, and when that object is close enough, to
turn on the LED.
As with the previous function, we need to run this one for each class instance by typing `classinstancename.controlLED();` where `classinstancename` is what we defined in the first section.
Again, aach instance of the class needs to be initialised in the `void loop()` block individually, eg:

`classinstancename1.controlLED();`

`classinstancename2.controlLED();`

`classinstancename3.controlLED();`

Now just upload your sketch to your Arduino and your done!
If you have problems with some LEDs staying on or not turning on, try adjusting the `proximityvalue` up or down respectively.

Raspberry Pi
------------

The Raspberry Pi is responsible for everything else in the project, this includes monitoring tweets, controlling the top of the tree light, playing media and serving the display via Node.js.

###Python
The code controlling the RGB LEDs on top of the tree and playing the Christmas MP3s is written in Python and can be found at `raspberrypi/TweetBlinkyRGB.py`.
It requires the Python Twitter library Twython to be installed on the Pi. https://github.com/ryanmcgrath/twython

We are only interested in tweets with certain keywords, not the whole of the streaming API. To filter this out, we need to add the keywords to the `TERMS` variable.
In the code file I am only looking for tweets containig at replies to certain users, but other options are available here, usernames, hashtags etc and more than one thing can be searched for at the same time, separated by commas, eg:

`TERMS = '@thinkingjuice,@weareemerge,@sephallen,@tjxmaspi,@ben_poulson,@dj10dj100'`

Next, very much like the Arduino, we assign the LED with variable names, making it easier if we change the pin number later on. The RGB LED we are using are technically three LED's in one, red, blue and green. Each colour has its own pin, eg:

`RED = 22`

`GREEN = 16`

`BLUE = 18`

The Twitter streaming api requires application authentication tokens, though for our purposes we do not need write access. Again, to make things easier we assign these tokens variable names here, eg:

`APP_KEY = ''`

`APP_SECRET = ''`

`OAUTH_TOKEN = ''`

`OAUTH_TOKEN_SECRET = ''`

Next comes all the functions that do different things, such as flash LEDs and play music. The project uses `mpg123` for MP3 playback on the Pi, you may need to install this separately by typing `sudo apt-get install mpg123` in the Pi terminal.

The `lightShow()` function cycles through all colours while an MP3 is playing, the cycle lasts for a total of seven seconds. To keep the light show going for the length of the song, divide the song length by seven and use a while loop to repeat the light show cycle that many times.

To play the MP3 and light show cycle simultaneously, one of them needs to be threaded. In the code I have threaded the MP3 playback.
If a certain hashtag is found within a tweet, the corresponding function is called.

To initialise the GPIO pins we want to use on the Pi, we need to set them up and put their output to low (off), eg:

`GPIO.setmode(GPIO.BOARD)`

`GPIO.setup(RED, GPIO.OUT)`

`GPIO.output(RED, GPIO.LOW)`

Using upstart (`sudo apt-get upstart`) we can set the Python script to run on boot in the background and if for some reason it crashes, the script will relaunch.

###Node.js
Node.js is used in this project for the web display on the TV. It also uses the Twitter streaming API to search for the same keywords as before and displays the tweet and media (pictures, YouTube videos, Vimeo videos and SoundCloud songs) via the TV.

Most of the setup can be found in `raspberrypi/TweetNode/server.js`.
This requires twit, a Node.js Twitter framework https://github.com/ttezel/twit Socket.io http://socket.io and express http://expressjs.com

A lot of the setup here is very similar to the Python script, but note that the Twitter api credentials are not the same. This is because Twitter does not allow two simultaneous instances of the streaming api on one account.

The keyword search list is held in `watchList`, eg:

`var watchList = ['@thinkingjuice,@weareemerge,@sephallen,@tjxmaspi,@ben_poulson,@dj10dj100'];`

For hashtags we can also set an animated .gif background, eg:

`var littleDonkey = turl.match(/littledonkey/gi)`

    `if ( littleDonkey != null ) {`

      `mediaUrl = 'http://share.gifyoutube.com/ZRMz66.gif'`

    `}`

And looking for other hashtags with valid IDs, we can embed different media on the display, eg:

`var youTube = turl.match(/#yt-/gi)`

    `if ( youTube != null ) {`

      `var str = turl;`

      `var regex = /#yt-([a-zA-Z0-9_-]{1,11})/gi;`

      `var matches = str.match(regex);`

      `var ytid = matches[0].replace("#yt-", "");`

      `turl = turl.concat( '<div class="youtube"><iframe src="//www.youtube.com/embed/'+ytid+'?autoplay=1" frameborder="0"></iframe></div>' );`

    `}`

`node-twitter-stream.css` and `node-twitter-stream.html` should be pretty self explanatory.

The `server.js` file is launched at boot using forever https://github.com/nodejitsu/forever and adding the command to the Pi's cron.

###Web GUI
The Web GUI was created to make it easier for users to find all the options and easily tweet the correct hashtags. It also strips media URLs down and gets the coreent IDs the Pi is looking for.

Twitter will not display in iframes, so each tweet will display in a pop up window.

The Web GUI uses Bootstrap http://getbootstrap.com

###Display
The Pi does boot to full screen Chromium showing the Node.js display, but due to the lack of GPU acceleration the performance is very low so it is not advised.
A good guide for setting this up can be found here http://blogs.wcode.org/2013/09/howto-boot-your-raspberry-pi-into-a-fullscreen-browser-kiosk/ but remember that the screen will need to be rotated.

For the MP3's, the sound comes directly from the Pi via HDMI or the audio jack output, so speakers will be required.
