pip install youtube-dl
import youtube_dl

url=input()

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl':  "sample_music" + '.%(ext)s',
    'postprocessors': [
        {'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
         'preferredquality': '192'},
        {'key': 'FFmpegMetadata'},
    ],
}

ydl = youtube_dl.YoutubeDL(ydl_opts)
info_dict = ydl.extract_info(url, download=True)
