from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongo:27017")

client = AsyncIOMotorClient(MONGO_URL)

master_db = client["master_db"]

admins_col = master_db["admins"]
organizations_col = master_db["organizations"]

# OPTIONAL alias to avoid breaking older imports:
orgs_col = organizations_col