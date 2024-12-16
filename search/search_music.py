import configparser
from yandex_music.exceptions import NotFoundError
from yandex_music import Client


config = configparser.ConfigParser()
config.read("CONFIG.ini")
ya_token = config["Passwords"]["YA_token"]

client = Client(ya_token).init()

type_to_name = {
    'track': 'трек',
    'artist': 'исполнитель',
    'album': 'альбом',
    'playlist': 'плейлист',
    'video': 'видео',
    'user': 'пользователь',
    'podcast': 'подкаст',
    'podcast_episode': 'эпизод подкаста',
}


def get_track(string):
    global filename, res
    search_result = client.search(string, playlist_in_best=False)

    if search_result.best and search_result.best.type == 'track':
        res = search_result.best.result
        artists = ''
        if res.artists:
            artists = ' - ' + ', '.join(artist.name for artist in res.artists)
        filename = res.title + artists
        text_for_person = 1
    else:
        text_for_person = 0
        filename = 0
    return filename, text_for_person


def download_track():
    for el in client.tracks_download_info(res.id, get_direct_links=True):
        if el['codec'] == 'mp3' and el['bitrate_in_kbps'] == 192:
            client._request.download(el['direct_link'], f"{filename}.mp3")
            try:
                lyrics = res.get_lyrics('LRC')
                text_track = lyrics.fetch_lyrics() + "\n" + f'\nИсточник: {lyrics.major.pretty_name}' + "\n"
            except NotFoundError:
                text_track = 'Текст песни отсутствует' + "\n"

            return text_track, filename
