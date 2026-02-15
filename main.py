import sys
import xbmcgui
import xbmcplugin

def main():
    handle = int(sys.argv[1])
    
    # Zoznam rádií (tu si môžeš pridávať ďalšie)
    radia = [
        {
            "nazov": "Fun Rádio",
            "url": "https://stream.funradio.sk:8000/fun128.mp3",
            "zaner": "Pop / Dance"
        },
        {
            "nazov": "Rádio Vlna",
            "url": "https://stream.radiovlna.sk/vlna-128.mp3",
            "zaner": "Oldies"
        }
    ]

    for radio in radia:
        # Vytvoríme položku so správnym názvom
        list_item = xbmcgui.ListItem(label=radio["nazov"])
        
        # Nastavíme informácie, aby Kodi vedelo, čo zobrazuje
        list_item.setInfo('video', {
            'title': radio["nazov"],
            'genre': radio["zaner"]
        })
        
        # Označíme, že ide o prehrateľný súbor (audio stream)
        list_item.setProperty('IsPlayable', 'true')
        
        # Pridáme do zoznamu
        xbmcplugin.addDirectoryItem(handle, radio["url"], list_item, False)

    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
