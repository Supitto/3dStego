ffmpeg -r 25 -f image2 -s 400x400 -i %d.png -vcodec libx264 -crf 1  -pix_fmt yuv420p video.mp4
