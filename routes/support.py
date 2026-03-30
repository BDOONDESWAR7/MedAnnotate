"""
SUPPORT & FEEDBACK ROUTES — Communication between doctors and companies
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from bson import ObjectId
from datetime import datetime
from utils.db import get_user_by_id

support_bp = Blueprint('support', __name__)

@support_bp.route('/my-companies', methods=['GET'])
@jwt_required()
def get_my_companies():
    """Returns a list of companies the current doctor has annotated for."""
    uid = get_jwt_identity()
    
    # Find active/completed annotations by this doctor
    annotations = list(mongo.db.annotations.find(
        {'doctor_id': ObjectId(uid)},
        {'image_id': 1}
    ))
    
    if not annotations:
        return jsonify({'companies': []}), 200
        
    image_ids = [a['image_id'] for a in annotations]
    
    # Find images to get company_ids
    images = list(mongo.db.images.find(
        {'_id': {'$in': image_ids}},
        {'company_id': 1, 'company_name': 1}
    ))
    
    # Extract unique companies
    companies_map = {}
    for img in images:
        cid = str(img.get('company_id'))
        name = img.get('company_name') or "Unknown Company"
        if cid and cid != 'None':
            companies_map[cid] = name
            
    result = [{'id': k, 'name': v} for k, v in companies_map.items()]
    return jsonify({'companies': result}), 200

@support_bp.route('/inquiry', methods=['POST'])
@jwt_required()
def submit_inquiry():
    """Doctors submit a new inquiry."""
    uid = get_jwt_identity()
    data = request.get_json()
    
    subject = data.get('subject')
    message = data.get('message')
    recipient_type = data.get('recipient_type', 'system') # 'system' or 'company'
    company_id = data.get('company_id')
    
    if not subject or not message:
        return jsonify({'error': 'Subject and message are required'}), 400
        
    doctor = get_user_by_id(uid)
    if not doctor:
        return jsonify({'error': 'Doctor not found'}), 404
        
    inquiry = {
        'doctor_id': ObjectId(uid),
        'doctor_name': doctor.get('name'),
        'recipient_type': recipient_type,
        'company_id': ObjectId(company_id) if company_id and recipient_type == 'company' and len(str(company_id)) == 24 else company_id if recipient_type == 'company' else None,
        'subject': subject,
        'message': message,
        'status': 'unread',
        'replies': [],
        'created_at': datetime.utcnow()
    }
    
    res = mongo.db.inquiries.insert_one(inquiry)
    return jsonify({'message': 'Inquiry submitted', 'id': str(res.inserted_id)}), 201

@support_bp.route('/mailbox', methods=['GET'])
@jwt_required()
def get_mailbox():
    """Admins see all 'system' inquiries, Companies see their directed inquiries."""
    uid = get_jwt_identity()
    user = get_user_by_id(uid)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403

    query = {}
    if user.get('role') == 'admin':
        query = {'recipient_type': 'system'}
    elif user.get('role') == 'company':
        query = {
            'recipient_type': 'company',
            '$or': [{'company_id': ObjectId(uid) if len(str(uid)) == 24 else None}, {'company_id': uid}]
        }
    else:
        return jsonify({'error': 'Unauthorized'}), 403
        
    inquiries = list(mongo.db.inquiries.find(query).sort('created_at', -1))
    for i in inquiries:
        i['id'] = str(i['_id'])
        del i['_id']
        i['doctor_id'] = str(i['doctor_id'])
        if i.get('company_id'): i['company_id'] = str(i['company_id'])
        if 'created_at' in i and not isinstance(i['created_at'], str): i['created_at'] = i['created_at'].isoformat()
        for r in i.get('replies', []):
            if 'sender_id' in r: r['sender_id'] = str(r['sender_id'])
            if 'created_at' in r and not isinstance(r['created_at'], str): r['created_at'] = r['created_at'].isoformat()
    
    return jsonify({'inquiries': inquiries}), 200

@support_bp.route('/inquiry/<id>/reply', methods=['POST'])
@jwt_required()
def reply_inquiry(id):
    """Admin/Company/Doctor replies to an inquiry thread."""
    uid = get_jwt_identity()
    user = get_user_by_id(uid)
    data = request.get_json()
    message = data.get('message')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
        
    reply = {
        'sender_id': str(uid),
        'sender_name': user.get('name'),
        'sender_role': user.get('role'),
        'message': message,
        'created_at': datetime.utcnow().isoformat()
    }
    
    query = {'$or': [{'_id': ObjectId(id) if len(str(id)) == 24 else None}, {'id': id}, {'_id': id}]}
    result = mongo.db.inquiries.update_one(
        query,
        {
            '$push': {'replies': reply},
            '$set': {'status': 'replied'}
        }
    )
    
    if result.modified_count == 0:
        return jsonify({'error': 'Inquiry not found or unable to update'}), 404
        
    return jsonify({'message': 'Reply sent'}), 200

@support_bp.route('/my-inquiries', methods=['GET'])
@jwt_required()
def get_my_inquiries():
    """Doctors see their past inquiries."""
    uid = get_jwt_identity()
    inquiries = list(mongo.db.inquiries.find({
        '$or': [{'doctor_id': ObjectId(uid) if len(str(uid)) == 24 else None}, {'doctor_id': uid}]
    }).sort('created_at', -1))
    
    for i in inquiries:
        i['id'] = str(i['_id'])
        del i['_id']
        i['doctor_id'] = str(i['doctor_id'])
        if i.get('company_id'): i['company_id'] = str(i['company_id'])
        if 'created_at' in i and not isinstance(i['created_at'], str): i['created_at'] = i['created_at'].isoformat()
        for r in i.get('replies', []):
            if 'sender_id' in r: r['sender_id'] = str(r['sender_id'])
            if 'created_at' in r and not isinstance(r['created_at'], str): r['created_at'] = r['created_at'].isoformat()
        
    return jsonify({'inquiries': inquiries}), 200
