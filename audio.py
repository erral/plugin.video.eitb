from utils import get_radio_programs
from utils import get_program_audios

import xbmcgui
import xbmcplugin


class AudioHandler(object):
    def __init__(self, handle, url):
        self.handle = handle
        self.url = url

    def list_radio_programs(self):
        listing = []
        for program in get_radio_programs():
            title = program.get('title')
            radio = program.get('radio')
            program_url = program.get('@id')
            # Create a list item with a text label and a thumbnail image.
            list_item = xbmcgui.ListItem(label=title)
            # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
            # Here we use the same image for all items for simplicity's sake.
            # In a real-life plugin you need to set each image accordingly.
            # list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
            #                   'icon': VIDEOS[category][0]['thumb'],
            #                   'fanart': VIDEOS[category][0]['thumb']})
            # Set additional info for the list item.
            # Here we use a category name for both properties for for simplicity's sake.
            # setInfo allows to set various information for an item.
            # For available properties see the following link:
            # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
            list_item.setInfo('music', {'title': title, 'album': radio})
            # Create a URL for the plugin recursive callback.
            # Example: plugin://plugin.video.example/?action=listing&category=Animals
            url = '{0}?action=audiolisting&program={1}'.format(self.url, program_url)
            # is_folder = True means that this item opens a sub-list of lower level items.
            is_folder = True
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_folder))
        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.handle)

    def list_program_audios(self, program):
        audios = get_program_audios(program)
        song_list = []
        for audio in audios:
            date = audio.get('date')
            title = audio.get('title')
            audio_url = audio.get('url')
            label = u'{0} ({1})'.format(date, title)
            # create a list item using the song filename for the label
            list_item = xbmcgui.ListItem(label=label)
            # set the fanart to the albumc cover
            # set the list item to playable
            list_item.setProperty('IsPlayable', 'true')
            # build the plugin url for Kodi
            url = '{0}?action=audioplay&program={1}'.format(self.url, audio_url)
            # is_folder = True means that this item opens a sub-list of lower level items.
            is_folder = False
            # Add our item to the listing as a 3-element tuple.
            song_list.append((url, list_item, is_folder))

        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.handle, song_list, len(song_list))
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.handle)

    def play_audio(self, path):
        # Create a playable item with a path to play.
        play_item = xbmcgui.ListItem(path=path)
        # Pass the item to the Kodi player.
        xbmcplugin.setResolvedUrl(self.handle, True, listitem=play_item)
