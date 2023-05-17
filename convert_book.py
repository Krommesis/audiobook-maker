#!/usr/bin/env python3


import os
import sys
import asyncio
import numpy as np
import argparse as ap
import pycld2 as cld2

from gtts import gTTS
from datetime import datetime
from pydub import AudioSegment
from nltk.tokenize import sent_tokenize
from pydub.silence import split_on_silence
from edge_tts import Communicate, VoicesManager


async def get_voice(lang: str) -> str:
    voices = await VoicesManager.create()
    voice = voices.find(Gender=sex.capitalize(), Language=lang)[0]["Name"]
    return voice


async def get_edge_audio(text: str, title: str, voice: str) -> None:
    communicate = Communicate(text, voice)
    await communicate.save(title)


def get_gtts_audio(text: str, title: str, lang: str) -> None:
    obj = gTTS(text=text, lang=lang, slow=False)
    obj.save(title)


def make_audios(sents: list, voice: str) -> None:
    """ Converts a list of sentences into a bunch of MP3 files. """

    sent_count = len(sents)
    for i in range(sent_count):
        sent = sents[i]
        num = (len(str(sent_count)) - len(str(i))) * '0' + str(i)
        title = f'{num} - {sent[:50]}.mp3'.replace('/', ' ')
        print(title)

        if os.path.exists(title):
            continue
        elif tts == "gtts":
            get_gtts_audio(sent, title, voice)
        else:
            asyncio.run(get_edge_audio(sent, title, voice))


def create_final_audio(book: str, filename: str) -> None:
    """ Converts a bunch of .mp3 audio files into one .mp3 file. """
    all_files = [f for f in os.listdir('./') if f.endswith('.mp3')]
    all_files.sort()
    combined = AudioSegment.silent(duration=1000)
    print("Concatenating audio files...")
    for file in all_files:
        combined = combined + AudioSegment.from_file(os.path.join("./", file))
    print("Final audio combined. Removing silence...")
    audio_chunks = split_on_silence(combined, min_silence_len = 300, silence_thresh = -45, keep_silence = 100,)
    audio = sum(audio_chunks)
    audio = np.array(audio.get_array_of_samples())
    combined = AudioSegment(audio.tobytes(), frame_rate=24000, sample_width=audio.dtype.itemsize, channels=1)
    combined = combined = AudioSegment.silent(duration=1000) + combined

    if not os.path.exists('ready/'):
        os.mkdir('ready')

    book = book.split(' - ')
    artist = book[0]
    album = book[1] if len(book) >= 2 else artist
    date = book[2] if len(book) > 2 else datetime.now().year
    genre = "Audiobook"
    composer = "audiobook-maker"
    tracknumber, *title = filename.split(' - ')
    title = ' - '.join(title) if len(title) > 1 else title[0]

    combined.export(os.path.join("ready/", f'{filename}.mp3'), bitrate="64k", format="mp3",
                    tags={"tracknumber": tracknumber, "title": title, "album": album,
                          "artist": artist, "date": date, "genre": genre, "composer": composer}
                    )
    print('MP3-file created!!!')
    #os.remove(file) os.rmdir(ir)
    os.system('rm *.mp3')


def main():
    print('Converting...')

    with open(book_file) as data:
        data = data.read()

    data = [d for d in data.split('\n===\n') if d not in ""]
    book = book_file.split('.txt')[0].strip()
    data_len = len(data)
    voice = None
    lang = None

    for i in range(len(data)):
        sys.stdout.write('\033c')
        sys.stdout.flush()
        text = data[i].replace('\n', ' ')
        name = data[i].split('\n')[0].strip()
        num = (len(str(data_len)) - len(str(i))) * '0' + str(i)
        name = name[:-1] if name.endswith('.') else name
        title = f'{num} - {name}'
        print(f'{data_len - i} - {name}\n')

        if os.path.exists(f"ready/{title}.mp3"):
            print('{audio} already exists!')
            continue
        else:
            langs = ['czech', 'danish', 'dutch', 'english', 'estonian', 'finnish', 'french',
                        'german', 'greek', 'italian', 'norwegian', 'polish', 'portuguese',
                        'russian', 'slovene', 'spanish', 'swedish', 'turkish']
            isReliable, textBytesFound, details = cld2.detect(text)
            if not lang:
                lang = (details[0][0].lower(), details[0][1])
            if not voice:
                if  tts == "edge":
                    voice = asyncio.run(get_voice(lang[1]))
                elif tts == "gtts":
                    voice = lang[1]

            sents = sent_tokenize(text, lang[0]) if lang[0] in langs else sent_tokenize(text)
            make_audios(sents, voice)
            create_final_audio(book, title)
            #quit()

    os.rename('ready/', book)
    print("Book conversion complited!!!")


if __name__ == '__main__':
    parser = ap.ArgumentParser(description="A simple program that converts text into audiobook.")
    parser.add_argument("-b", "--book", type=str, default=None, required=True,
                        help="location of the (b)ook to convert.")
    parser.add_argument("-s", "--tts", type=str, default="edge", choices=["gtts", "edge"],
                        help="speech (s)ynthesis selection")
    parser.add_argument("-g", "--gender", type=str, default="female", choices=["male", "female"],
                        help="select voice (g)ender for edge-tts")
    args = parser.parse_args()
    book_file = args.book
    tts = args.tts
    sex = args.gender
    main()
