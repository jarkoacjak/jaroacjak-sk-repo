import sys
import urllib.parse
import xbmcgui
import xbmcplugin

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    handle = int(sys.argv[1])
    arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
    params = dict(urllib.parse.parse_qsl(arg_string))

    if not params:
        # Hlavné menu TV
        url = build_url({'mode': 'list_tv'})
        li = xbmcgui.ListItem(label="[B]Slovenské a České TV[/B]")
        xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    elif params.get('mode') == 'list_tv':
        # Zoznam staníc
        tv_channels = [
            {"name": "TA3", "url": "https://live.ta3.com/live/ta3/ta3.m3u8", "logo": "https://www.ta3.com/img/logo-ta3.png"},
            {"name": "JOJ 24", "url": "https://live.joj.sk/hls/joj24-720.m3u8", "logo": "https://upload.wikimedia.org/wikipedia/sk/0/03/JOJ_24_logo.png"}
        ]
        for tv in tv_channels:
            li = xbmcgui.ListItem(label=tv["name"])
            li.setArt({'thumb': tv["logo"], 'icon': tv["logo"]})
            li.setInfo('video', {'title': tv["name"], 'mediatype': 'video'}) # DÔLEŽITÉ: video
            li.setProperty('IsPlayable', 'true')
            xbmcplugin.addDirectoryItem(handle, tv["url"], li, False)
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
