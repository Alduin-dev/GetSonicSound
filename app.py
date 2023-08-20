from pytube import Playlist
from pydub import AudioSegment
import os
import requests
import io
from tqdm import tqdm

# Ingresa la URL para descargar el playlist
playlist_url = 'https://www.youtube.com/playlist?list=PLHRfWmB-cTz-fopGK4LxferxnVKokgglm'

playlist = Playlist(playlist_url)

mp3_folder = 'playlistMusic'

if not os.path.exists(mp3_folder):
    os.makedirs(mp3_folder)

for video in playlist.videos:
    print(f'Descargando: {video.title}')
    
    audio_stream = video.streams.filter(only_audio=True).first()
    
    response = requests.get(audio_stream.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    mp3_path = os.path.join(mp3_folder, f'{video.title}.mp3')
    
    with open(mp3_path, 'wb') as f, tqdm(
        desc=video.title,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            f.write(data)
            bar.update(len(data))

print('Descarga completada.')