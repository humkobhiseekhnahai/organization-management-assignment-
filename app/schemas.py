from pydantic import BaseModel, EmailStr, Field

class OrgCreate(BaseModel):
    organization_name: str = Field(..., min_length=2)
    email: EmailStr
    password: str = Field(..., min_length=6)

class OrgGet(BaseModel):
    organization_name: str

class OrgUpdate(BaseModel):
    organization_name: str
    new_organization_name: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str