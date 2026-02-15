import sys
import xbmcgui
import xbmcplugin

def main():
    handle = int(sys.argv[1])
    
    # AKTUALIZOVANÝ ZOZNAM RÁDIÍ
    radia = [
        {
            "nazov": "Rádio Beta",
            "url": "http://stream.betaradio.sk:8000/128.mp3",
            "logo": "https://www.betaradio.sk/wp-content/themes/beta-radio/img/logo.png",
            "zaner": "Regionálne / Mix"
        },
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
        
        # Logá a ikonky
        list_item.setArt({
            'thumb': radio["logo"],
            'icon': radio["logo"]
        })
        
        # Informácie o stope
        list_item.setInfo('video', {
            'title': radio["nazov"],
            'genre': radio["zaner"]
        })
        
        # Dôležité pre streamovanie
        list_item.setProperty('IsPlayable', 'true')
        
        # Pridanie do zoznamu Kodi
        xbmcplugin.addDirectoryItem(handle, radio["url"], list_item, False)

    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
