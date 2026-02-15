import sys
import xbmcgui
import xbmcplugin

def main():
    handle = int(sys.argv[1])
    # Tu je tvoje rádio
    url = "https://stream.funradio.sk:8000/fun128.mp3"
    list_item = xbmcgui.ListItem(label="Zapnúť Moje Rádio")
    xbmcplugin.addDirectoryItem(handle, url, list_item, False)
    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
  
