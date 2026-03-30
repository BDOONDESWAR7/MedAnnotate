import sys
import os
sys.path.append(os.getcwd())
try:
    from app import create_app
    from extensions import mongo
    app = create_app()
    with app.app_context():
        pipeline = [
            {"$group": {"_id": "$id", "count": {"$sum": 1}, "docs": {"$push": "$_id"}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        dups = list(mongo.db.images.aggregate(pipeline))
        print(f"Found {len(dups)} duplicate IDs")
        for d in dups:
            print(f"ID: {d['_id']} (Found {d['count']} times)")
            for doc_id in d['docs']:
                doc = mongo.db.images.find_one({"_id": doc_id}, {"filename": 1, "created_at": 1, "company_id": 1})
                print(f"  - {doc_id}: {doc.get('filename')} ({doc.get('created_at')})")
except Exception as e:
    print(f"Error: {e}")
