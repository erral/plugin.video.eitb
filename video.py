from utils import get_programs
from utils import get_episodes
from utils import get_videos

import xbmcgui
import xbmcplugin


class VideoHandler(object):
    def __init__(self, handle, url):
        self.handle = handle
        self.url = url

    def list_programs(self):
        """
        Create the list of video programs in the Kodi interface.
        """
        programs = get_programs()
        # Create a list for our items.
        listing = []
        # Iterate through categories
        for program in programs:
            title = program.get('title')
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
            list_item.setInfo('video', {'title': title})
            # Create a URL for the plugin recursive callback.
            # Example: plugin://plugin.video.example/?action=listing&category=Animals
            url = '{0}?action=videolisting&program={1}'.format(self.url, program_url)
            # is_folder = True means that this item opens a sub-list of lower level items.
            is_folder = True
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_folder))
        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.handle)

    def list_episodes(self, url):
        """
        Create the list of episodes for a given program
        """
        listing = []
        episodes = get_episodes(url)
        for episode in episodes:
            title = episode.get('title')
            date = episode.get('broadcast_date', '')
            try:
                date = date.split('T')[0]
                title = u'{} ({})'.format(episode.get('title'), date)
            except:
                title = episode.get('title')

            desc = episode.get('description')
            episode_url = episode.get('@id')
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
            list_item.setInfo('video', {'title': title, 'plot': desc})
            # Create a URL for the plugin recursive callback.
            # Example: plugin://plugin.video.example/?action=listing&category=Animals
            url = '{0}?action=videoepisode&program={1}'.format(self.url, episode_url)
            # is_folder = True means that this item opens a sub-list of lower level items.
            is_folder = True
            # Add our item to the listing as a 3-element tuple.
            listing.append((url, list_item, is_folder))
        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.handle)

    def list_videos(self, url):
        """
        Create the list of playable videos in the Kodi interface.

        :param category: str
        """
        # Get the list of videos in the category.
        videos = get_videos(url)
        # Create a list for our items.
        listing = []
        # Iterate through videos.
        for video in videos.get('formats'):
            if video.get('ext') == 'mp4':
                title = u'{0} ({1})'.format(video['format'], videos['title'])
                # Create a list item with a text label and a thumbnail image.
                list_item = xbmcgui.ListItem(label=title)
                # Set additional info for the list item.
                list_item.setInfo('video', {'title': title})
                # Set graphics (thumbnail, fanart, banner, poster, landscape etc.) for the list item.
                # Here we use the same image for all items for simplicity's sake.
                # In a real-life plugin you need to set each image accordingly.
                list_item.setArt({'thumb': videos['thumbnail'], 'icon': videos['thumbnail'], 'fanart': videos['thumbnail']})
                # Set 'IsPlayable' property to 'true'.
                # This is mandatory for playable items!
                list_item.setProperty('IsPlayable', 'true')
                # Create a URL for the plugin recursive callback.
                # Example: plugin://plugin.video.example/?action=play&video=http://www.vidsplay.com/vids/crab.mp4
                url = '{0}?action=videoplay&video={1}'.format(self.url, video['url'])
                # Add the list item to a virtual Kodi folder.
                # is_folder = False means that this item won't open any sub-list.
                is_folder = False
                # Add our item to the listing as a 3-element tuple.
                listing.append((url, list_item, is_folder))
        # Add our listing to Kodi.
        # Large lists and/or slower systems benefit from adding all items at once via addDirectoryItems
        # instead of adding one by ove via addDirectoryItem.
        xbmcplugin.addDirectoryItems(self.handle, listing, len(listing))
        # Add a sort method for the virtual folder items (alphabetically, ignore articles)
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        # Finish creating a virtual folder.
        xbmcplugin.endOfDirectory(self.handle)

    def play_video(self, path):
        """
        Play a video by the provided path.

        :param path: str
        """
        # Create a playable item with a path to play.
        play_item = xbmcgui.ListItem(path=path)
        # Pass the item to the Kodi player.
        xbmcplugin.setResolvedUrl(self.handle, True, listitem=play_item)
