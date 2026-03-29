from app import create_app
from extensions import mongo
from bson import ObjectId

app = create_app()

import json
from bson import json_util

with app.app_context():
    data = {
        'images': list(mongo.db.images.find()),
        'users': list(mongo.db.users.find()),
        'annotations': list(mongo.db.annotations.find())
    }
    print(json_util.dumps(data, indent=2))
