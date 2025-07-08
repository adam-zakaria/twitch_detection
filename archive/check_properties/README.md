This effort of checking properties on download has been abandoned because it is challenging to not possible. Because:
* Streamers are not always online and there is no hook for on_download.
* twitch hls playlists do not necessarily accurately reflect the underlying encodings (and they're not meant to). Apparently yt-dlp does some inferring.
* even just knowning the file name is a pain - there is the yt-dlp encoding %(ext) business, .mp4.part, and whatever else.