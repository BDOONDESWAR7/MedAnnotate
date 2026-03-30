import sys
import os
sys.path.append(os.getcwd())
try:
    from app import create_app
    app = create_app()
    print("--- REGISTERED ROUTES ---")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule} [{', '.join(rule.methods)}]")
    print("--- END ---")
except Exception as e:
    print(f"Error: {e}")
