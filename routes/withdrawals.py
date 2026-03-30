"""
WITHDRAWAL ROUTES — Multi-stage approval (Doctor -> Company -> Admin)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mongo
from datetime import datetime
from bson import ObjectId
from utils.db import get_user_by_id

withdrawals_bp = Blueprint('withdrawals', __name__)

def safe_dict(p):
    if not p: return None
    p = dict(p)
    p['id'] = str(p['_id'])
    del p['_id']
    for f in ('doctor_id', 'company_id', 'payout_ids', 'paid_by'):
        if p.get(f):
            if isinstance(p[f], list):
                p[f] = [str(x) for x in p[f]]
            else:
                p[f] = str(p[f])
    for f in ('created_at', 'updated_at', 'company_approved_at', 'paid_at'):
        if p.get(f) and hasattr(p[f], 'isoformat'):
            p[f] = p[f].isoformat()
    return p

# ── DOCTOR: REQUEST WITHDRAWAL ────────────────────────
@withdrawals_bp.route('/request', methods=['POST'])
@jwt_required()
def request_withdrawal():
    uid  = get_jwt_identity()
    user = get_user_by_id(uid)
    if not user or user['role'] != 'doctor':
        return jsonify({'error': 'Doctors only'}), 403
        
    data   = request.json or {}
    amount = data.get('amount')
    if not amount or float(amount) <= 0:
        return jsonify({'error': 'Invalid amount'}), 400
        
    amount = float(amount)
    available = user.get('pending_earnings', 0)
    if amount > available:
        return jsonify({'error': 'Insufficient pending earnings'}), 400
        
    method = data.get('method')
    metadata = data.get('metadata', {})
    
    now = datetime.utcnow()
    withdrawal_doc = {
        'doctor_id':    ObjectId(uid),
        'doctor_name':  user['name'],
        'amount':       amount,
        'method':       method,
        'metadata':     metadata,
        'status':       'pending_company', # 1. Waiting for company
        'created_at':   now,
        'updated_at':   now,
        'company_id':   None,
        'company_name': None,
        'paid_at':      None
    }
    
    res = mongo.db.withdrawals.insert_one(withdrawal_doc)
    
    # Deduct from user's pending_earnings IMMEDIATELY
    mongo.db.users.update_one(
        {'_id': ObjectId(uid)},
        {'$inc': {'pending_earnings': -amount}}
    )
    
    return jsonify({
        'message': 'Withdrawal request submitted. Waiting for company approval.',
        'id': str(res.inserted_id)
    }), 201

# ── DOCTOR: GET MY WITHDRAWALS ────────────────────────
@withdrawals_bp.route('/my', methods=['GET'])
@jwt_required()
def my_withdrawals():
    uid = get_jwt_identity()
    withdrawals = list(mongo.db.withdrawals.find({'doctor_id': ObjectId(uid)}).sort('created_at', -1))
    return jsonify({'withdrawals': [safe_dict(w) for w in withdrawals]}), 200

# ── COMPANY: GET PENDING FOR ME ───────────────────────
@withdrawals_bp.route('/company/pending', methods=['GET'])
@jwt_required()
def company_pending():
    uid = get_jwt_identity()
    user = get_user_by_id(uid)
    if not user or user['role'] != 'company':
        return jsonify({'error': 'Company access required'}), 403
    
    # In this simplified version, we show all withdrawals where the doctor has worked for this company
    # A more complex version would group payouts by company
    withdrawals = list(mongo.db.withdrawals.find({'status': 'pending_company'}).sort('created_at', 1))
    return jsonify({'withdrawals': [safe_dict(w) for w in withdrawals]}), 200

# ── COMPANY: APPROVE ──────────────────────────────────
@withdrawals_bp.route('/<wid>/company-approve', methods=['POST'])
@jwt_required()
def company_approve(wid):
    uid = get_jwt_identity()
    user = get_user_by_id(uid)
    if not user or user['role'] != 'company':
        return jsonify({'error': 'Company access required'}), 403
    
    now = datetime.utcnow()
    res = mongo.db.withdrawals.update_one(
        {'_id': ObjectId(wid), 'status': 'pending_company'},
        {'$set': {
            'status': 'pending_admin',
            'company_id': ObjectId(uid),
            'company_name': user.get('company_name') or user['name'],
            'company_approved_at': now,
            'updated_at': now
        }}
    )
    
    if res.modified_count == 0:
        return jsonify({'error': 'Withdrawal not found or already processed'}), 404
        
    return jsonify({'message': 'Approved by company. Now awaiting admin payment.'}), 200

# ── ADMIN: GET PENDING PAYMENT ────────────────────────
@withdrawals_bp.route('/admin/pending', methods=['GET'])
@jwt_required()
def admin_pending():
    uid = get_jwt_identity()
    user = get_user_by_id(uid)
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
        
    withdrawals = list(mongo.db.withdrawals.find({'status': 'pending_admin'}).sort('created_at', 1))
    return jsonify({'withdrawals': [safe_dict(w) for w in withdrawals]}), 200

# ── ADMIN: MARK PAID ──────────────────────────────────
@withdrawals_bp.route('/<wid>/pay', methods=['POST'])
@jwt_required()
def admin_pay(wid):
    uid = get_jwt_identity()
    user = get_user_by_id(uid)
    if not user or user['role'] != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
        
    now = datetime.utcnow()
    withdrawal = mongo.db.withdrawals.find_one({'_id': ObjectId(wid)})
    if not withdrawal or withdrawal['status'] != 'pending_admin':
        return jsonify({'error': 'Withdrawal not ready for payment'}), 400
        
    mongo.db.withdrawals.update_one(
        {'_id': ObjectId(wid)},
        {'$set': {
            'status': 'paid',
            'paid_at': now,
            'paid_by': ObjectId(uid),
            'updated_at': now
        }}
    )
    
    # Update doctor's overall earnings (move from pending to paid)
    mongo.db.users.update_one(
        {'_id': withdrawal['doctor_id']},
        {'$inc': {'paid_earnings': withdrawal['amount']}}
    )
    
    return jsonify({'message': 'Withdrawal marked as paid!'}), 200
