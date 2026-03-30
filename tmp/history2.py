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
                    # We want updates on 2026-03-30 specifically in the 03:00 to 04:00 range
                    if dt.year == 2026 and dt.month == 3 and dt.day == 30:
                        hour = dt.hour
                        minute = dt.minute
                        # "before 3:50" means hour <= 3 and minute <= 50, OR hour < 3.
                        # We want all updates today <= 3:50.
                        if hour < 3 or (hour == 3 and minute <= 50):
                            results.append({
                                'dt': dt.strftime('%H:%M:%S'), 
                                'uri': file_uri.replace('file:///c%3A/Users/VISSU/OneDrive/Pictures/Doondi/medical/medical/', ''), 
                                'path': os.path.join(os.path.dirname(entry_file), entry.get('id')),
                                'ts': ts
                            })
    except Exception as e:
        pass

# Deduplicate by uri, keeping the most recent one <= 3:50
latest_by_uri = {}
for r in results:
    uri = r['uri']
    if uri not in latest_by_uri or r['ts'] > latest_by_uri[uri]['ts']:
        latest_by_uri[uri] = r

sorted_results = sorted(latest_by_uri.values(), key=lambda x: x['ts'], reverse=True)
for r in sorted_results:
    print(f"{r['dt']} - {r['uri']} -> {r['path']}")

# Also let's print ALL versions of files modified exactly AT 3:50 just to be sure
print("--- EXACTLY AROUND 3:50 AM ---")
for r in sorted([x for x in results if x['dt'].startswith('03:49') or x['dt'].startswith('03:50')], key=lambda x: x['ts']):
    print(f"{r['dt']} - {r['uri']} -> {r['path']}")
