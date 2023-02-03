import os
import shutil
from io import BytesIO
from tempfile import TemporaryDirectory
import youtube_dl
from spleeter.separator import Separator
from pydub import AudioSegment


def make_downloader(tmp_dir):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': tmp_dir + '/song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    return ydl


def download_and_split(url) -> dict:
    with TemporaryDirectory() as tmp_dir:
        os.makedirs(tmp_dir, exist_ok=True)
        ydl = make_downloader(tmp_dir)

        ydl.download([url])

        separator = Separator('spleeter:5stems-16kHz')
        separator.separate_to_file(f'{tmp_dir}/song.mp3', f'{tmp_dir}/', codec='mp3')

        sources = dict(
            bass=AudioSegment.from_file(f"{tmp_dir}/song/bass.mp3", format="mp3"),
            drums=AudioSegment.from_file(f"{tmp_dir}/song/drums.mp3", format="mp3"),
            other=AudioSegment.from_file(f"{tmp_dir}/song/other.mp3", format="mp3"),
            piano=AudioSegment.from_file(f"{tmp_dir}/song/piano.mp3", format="mp3"),
            vocals=AudioSegment.from_file(f"{tmp_dir}/song/vocals.mp3", format="mp3"),
        )
    # shutil.rmtree(tmp_dir)
    return sources


def join_parts(parts, part_names):
    music = parts[part_names[0]]
    for part_name in part_names[1:]:
        music = music.overlay(parts[part_name])

    buffer = BytesIO()
    music.export(buffer, format="mp3")

    return buffer


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=sTGKOSXYXwU"

    parts = ['bass',
             'drums',
             'piano',
             'vocals',
             # 'other',
             ]

    sounds = download_and_split(url)
    result_bytes = join_parts(sounds, parts)

    with open('no_guitar_from_bytes.mp3', 'wb') as outfile:
        outfile.write(result_bytes.read())
