import os, json, glob
from datetime import datetime
appdata = os.environ.get('APPDATA')
history_dir = os.path.join(appdata, 'Code', 'User', 'History')
results = []
for entry_file in glob.glob(os.path.join(history_dir, '*', 'entries.json')):
    try:
        data = json.load(open(entry_file, 'r', encoding='utf-8'))
        file_uri = data.get('resource', '')
        if 'medical' in file_uri:
            entries = data.get('entries', [])
            if entries:
                for entry in entries:
                    ts = entry.get('timestamp', 0) / 1000.0
                    dt = datetime.fromtimestamp(ts)
                    results.append({'dt': dt.strftime('%Y-%m-%d %H:%M:%S'), 'uri': file_uri.split('/')[-1], 'id': entry.get('id'), 'parent': os.path.dirname(entry_file)})
    except Exception as e:
        pass

results.sort(key=lambda x: x['dt'], reverse=True)
for r in results[:30]:
    print(f"{r['dt']} - {r['uri']} -> {os.path.join(r['parent'], r['id'])}")
