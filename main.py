import sys
import urllib.parse
import xbmcgui
import xbmcplugin
import xbmc

# Funkcia na vytvorenie URL odkazov v menu
def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

# Funkcia, ktorá vypýta meno a heslo hneď po kliknutí na doplnok
def prihlasenie():
    dialog = xbmcgui.Dialog()
    
    # Okno pre používateľské meno
    user = dialog.input('Prihlásenie - Zadajte meno:', type=xbmcgui.INPUT_ALPHANUM)
    if not user: return None, None
    
    # Okno pre heslo (text bude skrytý hviezdičkami)
    password = dialog.input('Prihlásenie - Zadajte heslo:', type=xbmcgui.INPUT_ALPHANUM, isPassword=True)
    if not password: return None, None
    
    return user, password

def main():
    handle = int(sys.argv[1])
    arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
    params = dict(urllib.parse.parse_qsl(arg_string))

    # Ak používateľ práve otvoril doplnok (sme v hlavnom menu)
    if not params:
        user, password = prihlasenie()

        # KONTROLA: Meno musí byť Admin a heslo Kanianka8
        if user == "Admin" and password == "Kanianka8":
            xbmcgui.Dialog().notification('Flow play', 'Vitaj, Admin!', xbmcgui.NOTIFICATION_INFO, 3000)
            zobraz_hlavne_menu(handle)
        else:
            # Ak sú údaje nesprávne, vypíšeme chybu a skončíme
            xbmcgui.Dialog().ok('Flow play: Prístup odmietnutý', 'Zadané údaje nie sú správne.\nSkúste to znova.')
            return
    else:
        # Ak už sme prihlásení a klikáme na kategórie (Relácie, Filmy...)
        spracuj_kategoriu(handle, params)

def zobraz_hlavne_menu(handle):
    # Zoznam tvojich kategórií
    kategorie = [
        {"label": "Relácie", "mode": "relacie"},
        {"label": "Logistika", "mode": "logistika"},
        {"label": "Filmy", "mode": "filmy"}
    ]

    for kat in kategorie:
        # [B] urobí text tučným
        li = xbmcgui.ListItem(label="[B]" + kat["label"] + "[/B]")
        url = build_url({'mode': kat['mode']})
        # True znamená, že položka sa správa ako priečinok
        xbmcplugin.addDirectoryItem(handle, url, li, True)
    
    xbmcplugin.endOfDirectory(handle)

def spracuj_kategoriu(handle, params):
    mode = params.get('mode')
    
    # Text, ktorý sa zobrazí v každej sekcii
    oznam = "Už čoskoro pripravujeme..."
    
    if mode == 'relacie':
        li = xbmcgui.ListItem(label="[I]Sekcia Relácie - " + oznam + "[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        
    elif mode == 'logistika':
        li = xbmcgui.ListItem(label="[I]Sekcia Logistika - " + oznam + "[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)
        
    elif mode == 'filmy':
        li = xbmcgui.ListItem(label="[I]Sekcia Filmy - " + oznam + "[/I]")
        xbmcplugin.addDirectoryItem(handle, "", li, False)

    xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
