from bson import ObjectId
from extensions import mongo

def get_user_by_id(uid, projection=None):
    """
    Robustly fetch a user by ID, checking both _id (ObjectId) and id (string/email).
    """
    if not uid:
        return None
    
    # 1. Try internal ObjectId lookup
    try:
        oid = ObjectId(uid)
        user = mongo.db.users.find_one({'_id': oid}, projection)
        if user: return user
    except:
        pass
    
    # 2. Try secondary id or email lookup (backward compatibility / demo data)
    user = mongo.db.users.find_one({'$or': [{'id': uid}, {'email': uid}]}, projection)
    return user

def get_image_by_id(img_id, projection=None):
    """
    Robustly fetch an image by ID, checking both _id and legacy id field.
    """
    if not img_id:
        return None
    
    try:
        oid = ObjectId(img_id)
        img = mongo.db.images.find_one({'_id': oid}, projection)
        if img: return img
    except:
        pass
        
    img = mongo.db.images.find_one({'id': img_id}, projection)
    return img
