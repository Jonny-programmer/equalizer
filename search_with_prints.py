import configparser
from yandex_music import Client
from yandex_music.exceptions import NotFoundError


config = configparser.ConfigParser()
config.read("CONFIG.ini")
TOKEN = config["Passwords"]["token"]

client = Client(TOKEN).init()

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


def search_track(string):
    search_result = client.search(string, playlist_in_best=False)

    if search_result.best and search_result.best.type == 'track':
        res = search_result.best.result

        artists = ''
        if res.artists:
            artists = ' - ' + ', '.join(artist.name for artist in res.artists)
        filename = res.title + artists
        ans = input(f"Нашлось \'{filename}\'.\nХотите скачать этот трек? Да/нет\n>>> ").lower()
        if ans == "да":
            for el in client.tracks_download_info(res.id, get_direct_links=True):
                if el['codec'] == 'mp3' and el['bitrate_in_kbps'] == 192:
                    client._request.download(el['direct_link'], f"{filename}.mp3")
                    try:
                        lyrics = res.get_lyrics('LRC')
                        print(lyrics.fetch_lyrics())

                        print(f'\nИсточник: {lyrics.major.pretty_name}')
                    except NotFoundError:
                        print('Текст песни отсутствует')

                    print(f"Скачан один трек! --> \'{filename}.mp3\'")
        else:
            string = input('Введите поисковый запрос: ').strip()
            if string:
                search_track(string)
            return 0

    print("Ничего не нашлось((")
    return 0


if __name__ == '__main__':
    search_track(input('Введите поисковый запрос: '))
