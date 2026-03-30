import os
import json

history_dir = r"C:\Users\VISSU\AppData\Roaming\Code\User\History"
targets = [
    "frontend/css/main.css",
    "frontend/index.html",
    "routes/annotations.py",
    "frontend/company/review.html",
    "demo_server.py"
]

found = []
for root, dirs, files in os.walk(history_dir):
    if "entries.json" in files:
        try:
            path = os.path.join(root, "entries.json")
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                resource = data.get("resource", "")
                if "medical" in resource:
                    for t in targets:
                        if t.replace("/", "\\") in resource.replace("/", "\\"):
                            entries = data.get("entries", [])
                            if entries:
                                last_entry = entries[-1]
                                entry_id = last_entry.get("id")
                                content_path = os.path.join(root, entry_id)
                                found.append((resource, content_path, last_entry.get("timestamp")))
        except Exception as e:
            pass

# Sort by timestamp descending
found.sort(key=lambda x: x[2], reverse=True)
for resource, content_path, ts in found:
    print(f"Resource: {resource}")
    print(f"Path: {content_path}")
    print(f"Timestamp: {ts}\n")
