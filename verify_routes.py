import sys
import os
sys.path.append(os.getcwd())
try:
    from app import create_app
    app = create_app()
    print("Listing ALL registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} ({rule.methods}) -> {rule.endpoint}")
except Exception as e:
    print(f"Error: {e}")
