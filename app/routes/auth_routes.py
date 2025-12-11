from fastapi import APIRouter, HTTPException
from app.db import admins_col
from app.utils.security import verify_password, create_jwt_token
from app.schemas import AdminLogin

router = APIRouter(tags=["auth"], prefix="/admin")

@router.post("/login")
async def admin_login(payload: AdminLogin):
    admin = await admins_col.find_one({"email": payload.email})
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, admin["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token({
        "admin_id": str(admin["_id"]),
        "organization": admin["organization_name"],
        "email": admin["email"]
    })

    return {"access_token": token, "token_type": "bearer"}