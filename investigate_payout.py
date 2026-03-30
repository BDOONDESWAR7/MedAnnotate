import sys
import os
from bson import ObjectId
sys.path.append(os.getcwd())
try:
    from app import create_app
    from extensions import mongo
    app = create_app()
    with app.app_context():
        # Look for the specific image reported in the log
        img_id = 'img-9ea3f482' # From log
        img = mongo.db.images.find_one({"id": img_id})
        if not img:
            print(f"FAILED: Image {img_id} not found in database.")
            # check if it exists by some other ID
            all_imgs = list(mongo.db.images.find(limit=5))
            print(f"Sample images: {[i.get('id') for i in all_imgs]}")
        else:
            print(f"SUCCESS: Image {img_id} found. _id: {img['_id']}, company_id: {img.get('company_id')}")
            
            # Now look for annotation with THIS image_id
            # We try both string and ObjectId
            q1 = {"image_id": img['_id']}
            q2 = {"image_id": str(img['_id'])}
            q3 = {"image_id": img_id}
            
            ann1 = mongo.db.annotations.find_one(q1)
            ann2 = mongo.db.annotations.find_one(q2)
            ann3 = mongo.db.annotations.find_one(q3)
            
            print(f"Annotation check (ObjectId): {'FOUND' if ann1 else 'NOT FOUND'}")
            print(f"Annotation check (str(ObjectId)): {'FOUND' if ann2 else 'NOT FOUND'}")
            print(f"Annotation check (id string): {'FOUND' if ann3 else 'NOT FOUND'}")
            
            if not any([ann1, ann2, ann3]):
                # List some annotations to see the format
                sample_anns = list(mongo.db.annotations.find(limit=3))
                print(f"Sample annotations format: {[{ 'image_id': str(a.get('image_id')), 'type': str(type(a.get('image_id'))) } for a in sample_anns]}")

except Exception as e:
    print(f"Error: {e}")
