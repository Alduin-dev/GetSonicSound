from pytube import YouTube
from pydub import AudioSegment
import os
import requests
import io

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    print(f"Descargando... {percentage:.2f}% completado", end='\r')

# Ingresa la URL del video o de la lista de reproducción
url = 'https://www.youtube.com/watch?v=HHOn8u-c2wk'

# Determina si es una URL de lista de reproducción o un video individual
is_playlist = 'playlist' in url

if is_playlist:
    from pytube import Playlist
    playlist = Playlist(url)
else:
    playlist = [url]  # Convierte el video individual en una lista

mp3_folder = 'music'

if not os.path.exists(mp3_folder):
    os.makedirs(mp3_folder)

for video_url in playlist:
    if is_playlist:
        video = playlist.get(url=video_url)
    else:
        video = YouTube(video_url, on_progress_callback=on_progress)

    print(f'Convirtiendo a MP3: {video.title}')
    
    audio_stream = video.streams.filter(only_audio=True).first()
    
    response = requests.get(audio_stream.url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    audio_content = b''
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            audio_content += chunk
            percentage = len(audio_content) / total_size * 100
            print(f"Descargando... {percentage:.2f}% completado", end='\r')
    
    audio = AudioSegment.from_file(io.BytesIO(audio_content))
    title = video.title if is_playlist else video.title + "_individual"
    mp3_path = os.path.join(mp3_folder, f'{title}.mp3')
    audio.export(mp3_path, format='mp3')
    print("Descarga completada: ", title)

print('Conversión a MP3 completada.')