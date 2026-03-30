import os, json, glob
from datetime import datetime

appdata = os.environ.get('APPDATA')
history_dir = os.path.join(appdata, 'Code', 'User', 'History')
output = open('tmp/all_history.txt', 'w', encoding='utf-8')

for entry_file in glob.glob(os.path.join(history_dir, '*', 'entries.json')):
    try:
        data = json.load(open(entry_file, 'r', encoding='utf-8'))
        file_uri = data.get('resource', '')
        if 'medical' in file_uri:
            for entry in data.get('entries', []):
                ts = entry.get('timestamp', 0) / 1000.0
                dt = datetime.fromtimestamp(ts)
                if dt.year == 2026 and dt.month == 3 and dt.day >= 29:
                    output.write(f"{dt} : {file_uri.split('/')[-1]} -> {entry.get('id')}\n")
    except Exception as e:
        pass
output.close()
