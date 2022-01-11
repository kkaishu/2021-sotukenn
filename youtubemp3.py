import youtube_dl
import streamlit as st

st.title("youtubeからmp3ファイルに変換してダウンロードするプログラムです。"）
st.header('下に変換したいyoutubeのURLを張り付けてください。もしかしたら時間がかかるかもです。')
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
