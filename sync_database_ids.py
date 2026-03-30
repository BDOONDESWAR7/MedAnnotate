import sys
import os
from bson import ObjectId
sys.path.append(os.getcwd())
try:
    from app import create_app
    from extensions import mongo
    app = create_app()
    with app.app_context():
        images = list(mongo.db.images.find({}))
        print(f"Syncing {len(images)} images...")
        for img in images:
            canonical_id = str(img['_id'])
            # Update the 'id' field to be the same as the MongoDB '_id'
            # This makes all identifiers globally unique and predictable.
            if img.get('id') != canonical_id:
                mongo.db.images.update_one({'_id': img['_id']}, {'$set': {'id': canonical_id}})
                # Also update annotations that point to the old id string
                old_id = img.get('id')
                if old_id:
                    res = mongo.db.annotations.update_many({'image_id': old_id}, {'$set': {'image_id': canonical_id}})
                    if res.modified_count > 0:
                        print(f"  - Updated {res.modified_count} annotations for image {old_id} -> {canonical_id}")
                print(f"  - Matched {img.get('filename')} to unique ID {canonical_id}")
        print("Database sync complete.")
except Exception as e:
    print(f"Error: {e}")
