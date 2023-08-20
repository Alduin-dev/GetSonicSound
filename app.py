from pytube import Playlist
from pydub import AudioSegment
import os
import requests
import io

playlist_url = 'https://www.youtube.com/playlist?list=PLHRfWmB-cTz-fopGK4LxferxnVKokgglm'

playlist = Playlist(playlist_url)

mp3_folder = 'mp3_conversions'

if not os.path.exists(mp3_folder):
    os.makedirs(mp3_folder)

for video in playlist.videos:
    print(f'Convirtiendo a MP3: {video.title}')
    
    audio_stream = video.streams.filter(only_audio=True).first()
    
    response = requests.get(audio_stream.url)
    audio_content = response.content
    
    audio = AudioSegment.from_file(io.BytesIO(audio_content))
    mp3_path = os.path.join(mp3_folder, f'{video.title}.mp3')
    audio.export(mp3_path, format='mp3')

print('Conversión a MP3 completada.')