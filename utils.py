import requests

API_URL = 'https://still-castle-99749.herokuapp.com'
VIDEO_PLAYLIST_URL = '{0}/playlist'.format(API_URL)
LAST_BROADCAST_VIDEO_PLAYLIST_URL = '{0}/last-broadcast-list'.format(API_URL)
RADIO_PLAYLIST_URL = '{0}/radio'.format(API_URL)
PROGRAM_TYPES_URL = '{0}/program-type-list'.format(API_URL)
PROGRAM_TYPES_PLAYLIST_URL = '{0}/type-playlist'.format(API_URL)


def get_programs():
    data = requests.get(VIDEO_PLAYLIST_URL)
    return data.json().get('member')


def get_programs_types():
    data = requests.get(PROGRAM_TYPES_URL)
    return data.json().get('member')


def get_programs_types_playlist(url):
    data = requests.get(url)
    return data.json().get('member')


def get_last_broadcast(items):
    data = requests.get('{0}?items={1}'.format(LAST_BROADCAST_VIDEO_PLAYLIST_URL, items))
    return data.json().get('member')

def get_episodes(url):
    data = requests.get(url)
    return data.json().get('member')


def get_videos(url):
    data = requests.get(url)
    return data.json()


def get_radio_programs():
    data = requests.get(RADIO_PLAYLIST_URL)
    return data.json().get('member')


def get_program_audios(url):
    data = requests.get(url)
    return data.json().get('member')
