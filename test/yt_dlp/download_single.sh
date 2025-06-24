#!/bin/bash

#yt-dlp --cookies cookies.txt --wait-for-video 600 -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/TchiKK -o "TchiKK.%(ext)s"
yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/TchiKK -o "TchiKK.%(ext)s"

pm2 start "yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/TchiKK -o 'streams/TchiKK.%(ext)s'"

pm2 start "yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/TriPPPeY -o 'streams/TriPPPeY.%(ext)s'"

pm2 start "yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/ItzTheLastShot -o 'streams/ItzTheLastShot.%(ext)s'"

pm2 start "yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/Preecisionn -o 'streams/Preecisionn.%(ext)s'"

pm2 start "yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/Preecisionn -o 'streams/Preecisionn.%(ext)s'"

pm2 start "yt-dlp --cookies cookies.txt -S 'vcodec:h265,acodec:aac' https://www.twitch.tv/Preecisionn -o 'streams/Preecisionn.%(ext)s'"
