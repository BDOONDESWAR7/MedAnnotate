import sys
import os
import uuid
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
        print(f"Cleaning up {len(dups)} duplicate clusters...")
        for cluster in dups:
            # Keep the first one as is, regenerate the others
            docs = cluster['docs']
            print(f"Cluster {cluster['_id']}: {len(docs)} documents")
            for i in range(1, len(docs)):
                new_id = f"img-{uuid.uuid4().hex[:12]}"
                doc_id = docs[i]
                mongo.db.images.update_one({"_id": doc_id}, {"$set": {"id": new_id}})
                print(f"  - Updated document {doc_id} with new ID: {new_id}")
        print("Cleanup complete.")
except Exception as e:
    print(f"Error: {e}")
