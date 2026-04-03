# Detailed Deployment Guide: AI Road Safety System

This guide outlines exactly how to take your AI Road Safety System from a local environment to a live, production-ready application.

Our stack consists of:
*   **Backend:** Python, FastAPI, SQLAlchemy, Scikit-Learn/XGBoost.
*   **Frontend:** React, Vite, Tailwind CSS.

We will use **Render** for the backend (free tier available) and **Vercel** for the frontend (free tier available). We will also migrate the local SQLite database to a **Supabase PostgreSQL** database.

---

## Phase 1: Code Preparation

Before uploading code to any servers, we must modify the application to handle production environments.

### 1. Database Migration (SQLite to PostgreSQL)
Local hosting relies on `sql_app.db` (SQLite). Cloud providers wipe local files on restart, so your data will be lost. We must use a cloud database.
1.  Sign up for [Supabase](https://supabase.com/) and create a new project.
2.  Go to Project Settings -> Database and copy the **PostgreSQL Connection Details** (Connection string/URI).
3.  **Code Change required in `backend/app/database.py`:**
    Modify the database connection to read from an Environment Variable rather than hardcoding SQLite:
    ```python
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

    # Fix for SQLAlchemy 1.4+ with Render/Heroku Postgres URLs
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # SQLite needs check_same_thread=False, Postgres doesn't
    if "sqlite" in SQLALCHEMY_DATABASE_URL:
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    ```

### 2. Configure CORS (Cross-Origin Resource Sharing)
Your backend must explicitly allow your frontend domain to communicate with it.
**Code Change required in `backend/app/main.py`:**
```python
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(...)

# Let the backend read the allowed origin from environment variables
origins = [
    "http://localhost:5173", # Local frontend
    os.getenv("FRONTEND_URL", "https://your-vercel-app-url.vercel.app") # Production frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 3. Frontend Environment Variables
The frontend currently fetches from `http://localhost:8000`. It needs to know the production backend URL when deployed.
1. In the `frontend` folder, create a file named `.env` locally.
2. Inside `frontend/src/api/axios.js` (or wherever you make requests), change the base URL to:
   ```javascript
   const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
   // Use this baseURL in Axios or Fetch
   ```

---

## Phase 2: Deploying the Backend (Render)

Render is an excellent platform for deploying Python/FastAPI applications via GitHub.

### 1. Create a `Procfile`
Create a file named exactly `Procfile` (no extension) inside the `backend` directory. Add this line:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
*(This tells Render commands to run your server and binds it to the cloud environment's port).*

### 2. Verify `requirements.txt`
Make sure `uvicorn` and `psycopg2-binary` (PostgreSQL driver) are in `backend/requirements.txt`:
```text
fastapi
uvicorn
sqlalchemy
psycopg2-binary
scikit-learn
xgboost
pandas
# ... (all other existing dependencies)
```

### 3. Push to GitHub
1. Initialize a Git repository in the root of your project: `git init`
2. Make sure you have a `.gitignore` to exclude `venv`, `node_modules`, `__pycache__`, and `*.db`.
3. Commit everything and push it to a new GitHub repository.

### 4. Deploy on Render
1. Go to [Render](https://render.com/) and click **New -> Web Service**.
2. Connect your GitHub account and select your repository.
3. Configure the service:
    *   **Root Directory:** `backend` (very important!)
    *   **Environment:** Python 3
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables:** Scroll down to Advanced -> Environment Variables and add:
    *   `DATABASE_URL`: *<Your Supabase Postgres URI>*
5. Click **Create Web Service**. 
6. Render will build and deploy. Once complete, it gives you a URL (e.g., `https://road-safety-api.onrender.com`).

---

## Phase 3: Deploying the Frontend (Vercel)

Now that the backend is live, we deploy the frontend to Vercel.

### 1. Connect Vercel to GitHub
1. Go to [Vercel](https://vercel.com/) and click **Add New Project**.
2. Import the exact same GitHub repository you used for the backend.

### 2. Configure the Frontend Build
1. **Framework Preset:** Vercel should automatically detect `Vite`.
2. **Root Directory:** Edit this and set it to `frontend` (very important!).
3. **Environment Variables:** Expand this section and add:
   *   Name: `VITE_API_URL`
   *   Value: `https://road-safety-api.onrender.com` *(Replace this with your actual Render URL from Phase 2)*

### 3. Deploy
Click **Deploy**. Vercel will run `npm install` and `npm run build`, then host your static files globally.
Once finished, you'll be given a live URL (e.g., `https://road-safety-platform.vercel.app`).

---

## Phase 4: Finalizing
1. Go back to your **Render** dashboard (Backend).
2. Update the Environment Variables on Render: Add `FRONTEND_URL` and set it to your new Vercel URL (`https://road-safety-platform.vercel.app`). This fixes CORS.
3. Restart your Render server.

Your entire system is now deployed! The public can visit the Vercel URL, which will communicate cleanly and securely with your backend and database.
