from app import create_app
from extensions import mongo
from collections import Counter

app = create_app()
with app.app_context():
    print("--- Image Database Audit ---")
    imgs = list(mongo.db.images.find({}, {'filename': 1, 'gridfs_id': 1}))
    total = len(imgs)
    gids = [str(i.get('gridfs_id')) for i in imgs if i.get('gridfs_id')]
    
    unique_gids = set(gids)
    counts = Counter(gids)
    
    print(f"Total Database Images: {total}")
    print(f"Total Unique Content (GridFS IDs): {len(unique_gids)}")
    
    if len(unique_gids) < total:
        print("\n[ALERT] DUPLICATION DETECTED!")
        for gid, count in counts.items():
            if count > 1:
                duplicate_files = [i.get('filename') for i in imgs if str(i.get('gridfs_id')) == gid]
                print(f"GID {gid}: Shared by {count} records: {duplicate_files}")
    else:
        print("\n[SUCCESS] No GridFS ID duplication found in metadata.")
