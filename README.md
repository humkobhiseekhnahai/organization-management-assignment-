# Organization Management Service (FastAPI + MongoDB + Docker)

A scalable, multi-tenant **Organization Management Service** built using **FastAPI**, **MongoDB**, and **Docker**.

This service allows:
- Creating organizations dynamically  
- Automatically generating admin users  
- Creating per-organization MongoDB collections  
- Updating organization names  
- Deleting organizations securely  
- Authenticating using JWT tokens  

---

## Key Features

### ✔ Organization Creation
- Creates an admin user with hashed password  
- Creates dynamic MongoDB collection: `org_<organization_name>`  
- Stores metadata in `organizations` collection  

### ✔ Admin Authentication
- JWT login  
- Verifies credentials securely  
- Returns token with admin + org information  

### ✔ Organization Update
- Renames organization  
- Renames dynamic Mongo collection  
- Updates admin references  

### ✔ Organization Deletion
- Validates admin ownership  
- Deletes dynamic collection  
- Removes metadata + admin entries  

---

## Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI |
| Database | MongoDB |
| Driver | Motor (async MongoDB driver) |
| Auth | JWT (PyJWT) |
| Deployment | Docker & Docker Compose |

---

# Project Structure

```
organization_service/
│── app/
│   ├── main.py
│   ├── db.py
│   ├── schemas.py
│   ├── utils/
│   │   └── security.py
│   └── routes/
│       ├── org_routes.py
│       └── auth_routes.py
│
│── Dockerfile
│── docker-compose.yml
│── requirements.txt
│── README.md
│── .env
```

---

# ⚙️ Setup Instructions

### Clone the repo

```bash
git clone <repo-url>
cd organization_service
```

---

### Create `.env` file

```
MONGO_URL=mongodb://mongo:27017
JWT_SECRET=your_secret_key
JWT_EXPIRES_IN=3600
MASTER_DB=master_db
```

---

### Run using Docker

```bash
docker-compose up --build
```

FastAPI will be live at:

```
http://localhost:8000
```

Swagger docs:

```
http://localhost:8000/docs
```

---

# API Endpoints

## ➤ Create Organization
```
POST /org/create
```
<img width="806" height="561" alt="Screenshot 2025-12-12 at 12 14 16 AM" src="https://github.com/user-attachments/assets/47cb7e3d-aab0-49d9-9158-15af46c3cf1d" />


Body:
```json
{
  "organization_name": "examplecorp",
  "email": "admin@example.com",
  "password": "admin123"
}
```

---

## ➤ Admin Login
```
POST /admin/login
```
<img width="812" height="581" alt="Screenshot 2025-12-12 at 12 15 44 AM" src="https://github.com/user-attachments/assets/5d2e7b22-0c77-4858-a3b9-23a4db6ba908" />

---

## ➤ Get Organization
```
GET /org/get?organization_name=examplecorp
```
<img width="824" height="607" alt="Screenshot 2025-12-12 at 12 14 45 AM" src="https://github.com/user-attachments/assets/50cfdfef-2e79-4f9d-b8f2-31d53fb61bde" />

---

## ➤ Update Organization
```
PUT /org/update
```
<img width="827" height="498" alt="Screenshot 2025-12-12 at 12 18 14 AM" src="https://github.com/user-attachments/assets/3293c1a0-a203-4476-8c99-68e0d44460fe" />

---

## ➤ Delete Organization
```
DELETE /org/delete?organization_name=examplecorp
```
<img width="813" height="551" alt="Screenshot 2025-12-12 at 1 19 44 AM" src="https://github.com/user-attachments/assets/402552d5-1ab0-47db-9ed3-2c19f771a07b" />


---

# Architecture Diagram


<img width="6594" height="1017" alt="Mermaid Chart - Create complex, visual diagrams with text -2025-12-11-201152" src="https://github.com/user-attachments/assets/28ba659a-c230-49e7-b2fb-5a50ccc3816c" />




MIT License.
