import sys
import xbmcgui
import xbmcplugin

def main():
    handle = int(sys.argv[1])
    
    # Zoznam rádií s URL adresami a LOGAMI
    radia = [
        {
            "nazov": "Rádio Expres",
            "url": "https://stream.expres.sk/128.mp3",
            "logo": "https://www.expres.sk/wp-content/themes/expres2017/img/logo-expres.png",
            "zaner": "Pop"
        },
        {
            "nazov": "Fun Rádio",
            "url": "https://stream.funradio.sk:8000/fun128.mp3",
            "logo": "https://www.funradio.sk/static/images/logo.png",
            "zaner": "Pop / Dance"
        },
        {
            "nazov": "Rádio Vlna",
            "url": "https://stream.radiovlna.sk/vlna-128.mp3",
            "logo": "https://www.radiovlna.sk/static/images/logo.png",
            "zaner": "Oldies"
        }
    ]

    for radio in radia:
        list_item = xbmcgui.ListItem(label=radio["nazov"])
        
        # Nastavenie loga (Art)
        list_item.setArt({
            'thumb': radio["logo"],
            'icon': radio["logo"],
            'fanart': radio["logo"]
        })
        
        # Nastavenie informácií
        list_item.setInfo('video', {
            'title': radio["nazov"],
            'genre': radio["zaner"]
        })
        
        list_item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, radio["url"], list_item, False)

    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
