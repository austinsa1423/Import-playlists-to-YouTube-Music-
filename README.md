Moved over to Youtube Music but you don’t want to manually add all your songs? Hope this help

You are here for one of two reasons. You are reviewing my Github for my coding ability or you are moved over to Youtube Music and realized that moving music streaming platforms is difficult because you have to move all you playlists over and that can be a ton of manual work. Trust me I can relate; this is my second time changing.

For my use case I moved from Spotify to Youtube Music. Now Spotify is great cause they have an API that you are able to use to export your songs. That is not what I did because that seemed like too much work but that is an option. I will show you my quick and dirty way of doing it (which will work for any web-based music platform) but seriously just use the API if you are coming from Spotify.

Once you have the songs for each playlist you will have to save them in this format to playlists.json. So each line is its on json object with a playlist with a string value with the playlist name and songs which is an array of song names and band names. Notice in these examples, there are no special characters. Anything that is not alphanumeric will cause the song to fail in the search. remove any special charterers before running. If it make sense replace the character with another ex. change BØRNS to BORNS 
{"playlist": "hecking sick tracks", "songs": ["You are my sunshine Johnny Cache", "Crazy Frog Axel F"]} 
{"playlist": "tracks that hecking sick", "songs": ["Wonderwall Oasis", "Skyrim Theme Song Wernetina1"]}

Now that you have the playlist in the right format. Let's get Python ready to rock. 

Other notes: If it seems to not be adding the songs to the playlist, update the XPaths where it seems to be getting stuck. All click actions are based on full XPaths since it seemed to get confused unless they were full ones.

