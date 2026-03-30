from extensions import mongo
from app import create_app
from bson import ObjectId

app = create_app()
with app.app_context():
    inqs = list(mongo.db.inquiries.find())
    for i in inqs:
        i['_id'] = str(i['_id'])
        if i.get('doctor_id'): i['doctor_id'] = str(i['doctor_id'])
        if i.get('company_id'): i['company_id'] = str(i['company_id'])
        if 'created_at' in i: i['created_at'] = str(i['created_at'])
    print(inqs)
