Moved over to Youtube Music but you don’t want to manually add all your songs? Hope this help

You are here for one of two reasons. You are reviewing my Github for my coding ability or you are moved over to Youtube Music and realized that moving music streaming platforms is difficult because you have to move all you playlists over and that can be a ton of manual work. Trust me I can relate; this is my second time changing.

For my use case I moved from Spotify to Youtube Music. Now Spotify is great cause they have an API that you are able to use to export your songs. That is not what I did because that seemed like too much work but that is an option. I will show you my quick and dirty way of doing it (which will work for any web-based music platform) but seriously just use the API if you are coming from Spotify.

Once you have the songs for each playlist you will have to save them in this format to playlists.json. So each line is its on json object with a playlist with a string value with the playlist name and songs which is an array of song names and band names. Notice in these examples, there are no special characters. Anything that is not alphanumeric will cause the song to fail in the search. remove any special charterers before running. If it make sense replace the character with another ex. change BØRNS to BORNS 

{"playlist": "hecking sick tracks", "songs": ["You are my sunshine Johnny Cache", "Crazy Frog Axel F"]} 
{"playlist": "tracks that hecking sick", "songs": ["Wonderwall Oasis", "Skyrim Theme Song Wernetina1"]}

Quick and Dirty way to do it is to copy the HTML table element from the playlist page. Hit F12, use the element selector tool to find the table element. Right click and copy the "inner html". Paste this into a text editor like Sublime and format it. If you have a long playlist, you will have to do this multiple times. Spotify will only show 100 songs at a time. Zoom all the way out in the window to display all 100. Copy the HTML and scroll down and copy the next set till you got them all. 

In the HTML there is a string that we can use to identify all songs title and bands "aria-label="Play ". Do a crtl + F and click find all. Hold shift and press home then ctrl + c to copy. Paste this into a new text editor window. Use crtl + F to clean up the excess code. Also take this time to remove any special characters. After this you can take this into Excel and remove the duplicates if there are any.

![spotify HTML] (https://i.imgur.com/tnCrdxO.png)

![sublime] (https://i.imgur.com/SEkRmXj.png)

Now that you have the playlists in the right format. Let's get Python ready to rock.

1. Install Python 2.7.13 that is located in the Setup folder

2. Add the environment variables for Python. Hit Windows + E > right click "This PC" > click "Advanced system settings" > "Advanced" > "Environment Variables" > Under "System variables" select "Path" > click "Edit > Add the following

C:\Python27\
C:\Python27\Scripts
C:\Python27\libs
C:\Python27\Lib
C:\Python27\DLLs

Back to the setup folder, run the Python Webscraping Libraries.bat to get the Python libs and Run the Twisted.msi (might not be needy but Scrapy used to be picky)

Download the chrome driver that matches your version of Chrome and place it in C:\Python27 or wherever you installed Python to

Python should be good to go now. Lets tweak something in the youtubeitem.py file

Open chrome go to chrome://version/ and copy Profile path. Paste this in the placeholder on line 35 but remove the "default" at the end. Dont forget to "\\" to escape the character 
options.add_argument("user-data-dir=<<enter chrome profile path here>>")
Ex. profile path - C:\\Users\\AustinsTotallyAwesomePC\\AppData\\Local\\Google\\Chrome\\User Data
  
You should now be good to run the program by opening Start Import.bat The program will pause and you will have to manually get signed into Youtube Music. Once you are ready, hit Enter to continue and the program will start the import!

Other notes: 
If it seems to not be adding the songs to the playlist, update the XPaths where it seems to be getting stuck. All click actions are based on full XPaths since it seemed to get confused unless they were full ones.

After the program finished, all the "failed" songs will be printed out. Those you will have to change the name of and run again or add them manually

Good Luck!
