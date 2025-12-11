from fastapi import APIRouter, HTTPException, Depends, Header
from app.schemas import OrgCreate, OrgGet, OrgUpdate
from app.db import master_db, orgs_col, admins_col, client
from app.utils.security import hash_password, decode_jwt_token
from bson.objectid import ObjectId

router = APIRouter(tags=["org"], prefix="/org")

def get_token_payload(authorization: str | None = Header(None)):
    # expects "Bearer <token>"
    if not authorization:
        raise HTTPException(401, "Missing Authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(401, "Invalid/Expired token")
    return payload

@router.post("/create")
async def create_org(payload: OrgCreate):
    name = payload.organization_name.strip().lower()

    # 1: Check if exists
    if await orgs_col.find_one({"organization_name": name}):
        raise HTTPException(400, "Organization already exists")

    # 2: Create collection
    collection_name = f"org_{name}"
    db = client[master_db.name]
    col = db[collection_name]
    await col.insert_one({"_init": True})
    await col.delete_many({"_init": True})

    # 3: Create admin
    hashed = hash_password(payload.password)
    admin_res = await admins_col.insert_one({
        "email": payload.email,
        "password": hashed,
        "organization_name": name
    })

    # 4: Insert org metadata
    org_doc = {
        "organization_name": name,
        "collection_name": collection_name,
        "admin_user_id": admin_res.inserted_id,
        "created_at": __import__("datetime").datetime.utcnow()
    }
    await orgs_col.insert_one(org_doc)

    return {
        "message": "Organization created",
        "organization_name": name,
        "collection_name": collection_name
    }
    name = payload.organization_name.strip().lower()
    # 1: uniqueness check
    if orgs_col.find_one({"organization_name": name}):
        raise HTTPException(400, "Organization already exists")

    # 2: dynamic collection name
    collection_name = f"org_{name}"
    db = client[master_db.name]  # same master DB, dynamic collections inside it
    # create collection if not exist (insert an init doc and delete it)
    col = db[collection_name]
    col.insert_one({"_init": True})
    col.delete_many({"_init": True})

    # 3: create admin user (hashed)
    hashed = hash_password(payload.password)
    admin_res = admins_col.insert_one({
        "email": payload.email,
        "password": hashed,
        "organization_name": name
    })

    # 4: store metadata
    org_doc = {
        "organization_name": name,
        "collection_name": collection_name,
        "admin_user_id": admin_res.inserted_id,
        "created_at": __import__("datetime").datetime.utcnow()
    }
    orgs_col.insert_one(org_doc)

    print("DEBUG ORG NAME CHECKED:", name)
    print("DEBUG FIND RESULT:", orgs_col.find_one({"organization_name": name}))

    # return minimal metadata
    return {
        "message": "Organization created",
        "organization_name": name,
        "collection_name": collection_name
    }

@router.get("/get")
async def get_org(organization_name: str):
    name = organization_name.strip().lower()

    org = await orgs_col.find_one({"organization_name": name})
    if not org:
        raise HTTPException(404, "Organization not found")

    org["admin_user_id"] = str(org["admin_user_id"])
    org["_id"] = str(org["_id"])

    return org
    name = organization_name.strip().lower()
    org = orgs_col.find_one({"organization_name": name})
    if not org:
        raise HTTPException(404, "Organization not found")
    org["admin_user_id"] = str(org["admin_user_id"])
    org["_id"] = str(org["_id"])
    return org

@router.put("/update")
def update_org(payload: OrgUpdate, token_payload: dict = Depends(get_token_payload)):
    # Require admin of that org
    org_name = payload.organization_name.strip().lower()
    new_name = payload.new_organization_name.strip().lower()
    if token_payload.get("organization") != org_name:
        raise HTTPException(403, "You are not admin of this organization")

    if orgs_col.find_one({"organization_name": new_name}):
        raise HTTPException(400, "New organization name already exists")

    org = orgs_col.find_one({"organization_name": org_name})
    if not org:
        raise HTTPException(404, "Organization not found")

    old_collection = org["collection_name"]
    new_collection = f"org_{new_name}"

    # Rename collection (atomic in Mongo)
    db = client[master_db.name]
    try:
        db[old_collection].rename(new_collection)
    except Exception as e:
        raise HTTPException(500, f"Failed to rename collection: {e}")

    # update admin record(s)
    admins_col.update_many({"organization_name": org_name}, {"$set": {"organization_name": new_name}})

    # update org metadata
    orgs_col.update_one({"organization_name": org_name}, {"$set": {"organization_name": new_name, "collection_name": new_collection}})

    return {"message": "Organization updated", "organization_name": new_name, "collection_name": new_collection}

@router.delete("/delete")
async def delete_org(organization_name: str, token_payload: dict = Depends(get_token_payload)):
    name = organization_name.strip().lower()

    # Only admin of org can delete
    if token_payload.get("organization") != name:
        raise HTTPException(403, "You are not admin of this organization")

    # ----------------------------
    # FIX: use await for async call
    # ----------------------------
    org = await orgs_col.find_one({"organization_name": name})
    if not org:
        raise HTTPException(404, "Organization not found")

    collection_name = org["collection_name"]
    db = client[master_db.name]

    # Drop collection
    try:
        await db.drop_collection(collection_name)
    except Exception as e:
        raise HTTPException(500, f"Failed to drop collection: {e}")

    # Delete metadata + admin users
    await admins_col.delete_many({"organization_name": name})
    await orgs_col.delete_one({"organization_name": name})

    return {"message": "Organization deleted", "organization_name": name}
    name = organization_name.strip().lower()
    # only admin of the org can delete
    if token_payload.get("organization") != name:
        raise HTTPException(403, "You are not admin of this organization")

    org = orgs_col.find_one({"organization_name": name})
    if not org:
        raise HTTPException(404, "Organization not found")

    # drop collection
    collection_name = org["collection_name"]
    db = client[master_db.name]
    try:
        db.drop_collection(collection_name)
    except Exception as e:
        raise HTTPException(500, f"Failed to drop collection: {e}")

    # delete metadata and admin(s)
    admins_col.delete_many({"organization_name": name})
    orgs_col.delete_one({"organization_name": name})

    return {"message": "Organization deleted", "organization_name": name}