from app import create_app
from extensions import mongo

app = create_app()
with app.app_context():
    imgs = list(mongo.db.images.find({}, {'filename': 1, 'gridfs_id': 1}).limit(20))
    for i in imgs:
        print(f"Name: {i.get('filename')} | GridFS_ID: {i.get('gridfs_id')}")
