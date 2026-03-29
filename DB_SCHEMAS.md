# MedAnnotate: Database Schemas (MongoDB)

This document defines the required structures for all MongoDB collections to ensure data integrity and perfect platform functionality.

---

## 1. `users` Collection
Stores all platform participants (Admins, Doctors, Companies).

```json
{
  "_id": "ObjectId",
  "id": "String (legacy lookup/email)",
  "name": "String",
  "email": "String (unique)",
  "password": "String (hashed)",
  "role": "Enum ['admin', 'doctor', 'company']",
  "verified": "Boolean",
  "active": "Boolean",
  "specialty": "String (Doctors only)",
  "license_number": "String (Doctors only)",
  "company_name": "String (Companies only)",
  "total_earnings": "Double",
  "pending_earnings": "Double",
  "paid_earnings": "Double",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

## 2. `images` Collection
Stores metadata for uploaded medical scans. Binary data is stored in GridFS.

```json
{
  "_id": "ObjectId",
  "id": "String (legacy UUID)",
  "filename": "String",
  "gridfs_id": "ObjectId (reference to fs.files)",
  "company_id": "ObjectId (ref: users)",
  "company_name": "String",
  "department": "String (e.g., Radiology)",
  "status": "Enum ['assigned', 'annotating', 'qa_review', 'approved']",
  "assigned_doctor_id": "ObjectId (ref: users)",
  "anonymized": "Boolean",
  "annotation_id": "ObjectId (ref: annotations, optional)",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

## 3. `annotations` Collection
Stores the actual clinical labels and findings for an image.

```json
{
  "_id": "ObjectId",
  "image_id": "ObjectId (ref: images)",
  "image_filename": "String",
  "doctor_id": "ObjectId (ref: users)",
  "doctor_name": "String",
  "department": "String",
  "labels": [
    {
      "type": "String",
      "value": "String",
      "confidence": "Double",
      "notes": "String"
    }
  ],
  "findings": "String (long text)",
  "status": "Enum ['draft', 'submitted', 'qa_approved']",
  "submitted_at": "ISODate",
  "qa_at": "ISODate",
  "qa_by": "ObjectId (ref: users, optional)"
}
```

## 4. `payouts` Collection
Tracks financial withdrawal requests from doctors.

```json
{
  "_id": "ObjectId",
  "doctor_id": "ObjectId (ref: users)",
  "amount": "Double",
  "status": "Enum ['pending', 'completed', 'cancelled']",
  "method": "Enum ['upi', 'bank']",
  "method_details": {
    "upi_id": "String",
    "bank_name": "String",
    "account_number": "String",
    "ifsc": "String"
  },
  "requested_at": "ISODate",
  "processed_at": "ISODate"
}
```

---
> [!IMPORTANT]
> All new records MUST use `ObjectId` for relational fields (`company_id`, `doctor_id`, `image_id`) to ensure the platform's robust dual-lookup logic functions correctly.
