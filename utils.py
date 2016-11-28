import xbmcaddon
import requests

addon = xbmcaddon.Addon()
API_URL = addon.getSetting('API_URL')
VIDEO_PLAYLIST_URL = '{0}/playlist'.format(API_URL)
RADIO_PLAYLIST_URL = '{0}/radio'.format(API_URL)


def get_programs():
    data = requests.get(VIDEO_PLAYLIST_URL)
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
