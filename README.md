
# ValerieBot

A Discord music bot I wrote for my Dungeons & Dragons server. While there are a lot of bots out there that allow streaming music from Youtube, I wanted a solution that allowed me to use local music, to have a greater control over the content without depending on random playlists or Youtube being up and working.

It's far from complete, and probably not really optimized, but it works well enough for me.

  

To work, it requires a `songs.json`file with the following format:

	{

		"song1": {

			"route": "music/song1.mp3",
		},
		"song2" : {
			"route": "music/song2.mp3",
			"start_point":"0:20",
			"end_point":"1:40"
		},
		[...],
		"playlist1" : [
			{"route":"music/song3.mp3"},
			{"route":"music/song4.mp3"},
			[...]
		]
	}

For faster use, it includes a helper script that reads every file from a folder and generates a playlist ready to be added to the songs.json file.

#### Why Valerie?
It is the name of a beloved Warforged NPC on my current campaign, and it seemed adequate enough for this!