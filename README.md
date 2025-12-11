# Organization Management Service (FastAPI + MongoDB + Docker)

## What
A simple multi-tenant-style backend that:
- Creates organizations (each with its own Mongo collection `org_<name>`)
- Stores metadata in a master DB
- Admin user creation and JWT authentication
- Update (rename) and delete organization

## Run (Docker)
1. Build & start:# organization-management-assignment-
