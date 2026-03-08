import sys
import urllib.parse
import xbmcgui
import xbmcplugin
from datetime import datetime, timedelta

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def main():
    try:
        handle = int(sys.argv[1])
        arg_string = sys.argv[2][1:] if len(sys.argv[2]) > 1 else ""
        params = dict(urllib.parse.parse_qsl(arg_string))
    except:
        return

    joj_headers = "|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36&Referer=https://videoportal.joj.sk/"
    now = datetime.now()

    # --- 1. HLAVNÉ MENU ---
    if not params:
        url_live = build_url({'mode': 'list_live_sk'})
        li_live = xbmcgui.ListItem(label="[B]📺 ŽIVÉ VYSIELANIE[/B]")
        xbmcplugin.addDirectoryItem(handle, url_live, li_live, True)

        url_archive = build_url({'mode': 'archive_days'})
        li_archive = xbmcgui.ListItem(label="[B]📂 ARCHÍV TV JOJ[/B]")
        xbmcplugin.addDirectoryItem(handle, url_archive, li_archive, True)

        xbmcplugin.endOfDirectory(handle)

    # --- 2. ŽIVÉ VYSIELANIE (EPG PODĽA ČASU) ---
    elif params.get('mode') == 'list_live_sk':
        program_joj = [
            {"time": "12:15", "title": "James Bond: Casino Royale"},
            {"time": "15:25", "title": "Hviezdy nad hlavou 9"},
            {"time": "16:45", "title": "Na chalupe"},
            {"time": "19:00", "title": "Krimi"},
            {"time": "19:30", "title": "Noviny TV JOJ"}
        ]
        
        current_show = "Program sa načítava..."
        for show in program_joj:
            st = datetime.strptime(show["time"], "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            if now >= st:
                current_show = show["title"]

        url_joj = "https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8" + joj_headers
        li = xbmcgui.ListItem(label=f"TV JOJ | [COLOR yellow]{current_show}[/COLOR]")
        li.setArt({'thumb': 'https://yt3.googleusercontent.com/8rPXBoj2l1nhd9C-DCXF-s3tx0i_36GJzJcxeMyYvyPpPNakQsyc5DYc5d_QLDeI74ILkmFSJQ=s900-c-k-c0x00ffffff-no-rj'})
        li.setInfo('video', {'title': "TV JOJ", 'plot': current_show})
        li.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(handle, url_joj, li, False)
        xbmcplugin.endOfDirectory(handle)

    # --- 3. ARCHÍV - VÝBER DŇA ---
    elif params.get('mode') == 'archive_days':
        for i in range(7):
            date_obj = now - timedelta(days=i)
            date_str = date_obj.strftime('%d.%m.%Y')
            label = f"Dnes ({date_str})" if i == 0 else date_str
            
            url = build_url({'mode': 'archive_list', 'date': date_str, 'day_offset': str(i)})
            li = xbmcgui.ListItem(label=label)
            xbmcplugin.addDirectoryItem(handle, url, li, True)
        xbmcplugin.endOfDirectory(handle)

    # --- 4. ARCHÍV - RELÁCIE (PREHRÁVANIE Z MINULOSTI) ---
    elif params.get('mode') == 'archive_list':
        date_str = params.get('date')
        day_offset = int(params.get('day_offset'))
        target_date = now - timedelta(days=day_offset)

        # Definícia programu s dĺžkou trvania (odhadovanou)
        vsetky_relacie = [
            {"time": "12:15", "duration": 180, "title": "James Bond: Casino Royale"},
            {"time": "15:25", "duration": 70,  "title": "Hviezdy nad hlavou 9"},
            {"time": "16:45", "duration": 60,  "title": "Na chalupe"},
            {"time": "19:00", "duration": 30,  "title": "Krimi"},
            {"time": "19:30", "duration": 45,  "title": "Noviny TV JOJ"}
        ]

        for r in vsetky_relacie:
            start_dt = datetime.strptime(r["time"], "%H:%M").replace(
                year=target_date.year, month=target_date.month, day=target_date.day)
            
            # Zobrazíme iba tie relácie, ktoré už skončili
            if now > (start_dt + timedelta(minutes=r["duration"])):
                # Výpočet UNIX timestampu pre archívny link
                start_ts = int(start_dt.timestamp())
                
                # Upravená URL pre archívne prehrávanie (timeshift)
                archive_url = f"https://live.cdn.joj.sk/live/andromeda/joj-1080.m3u8?start={start_ts}" + joj_headers
                
                label = f"{r['time']} - {r['title']}"
                li = xbmcgui.ListItem(label=label)
                li.setInfo('video', {'title': r['title'], 'plot': f"Vysielané: {date_str} o {r['time']}"})
                li.setProperty('IsPlayable', 'true')
                xbmcplugin.addDirectoryItem(handle, archive_url, li, False)
            
        xbmcplugin.endOfDirectory(handle)

if __name__ == '__main__':
    main()
    
