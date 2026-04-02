# Finance Data Processing and Access Control System Backend

This repository contains the backend for a Finance Data Processing and Access Control System, built with **FastAPI** and integrated with **Supabase (PostgreSQL)** using `supabase-py`.

## 🧱 Tech Stack
- **FastAPI**: Modern, fast web framework for building APIs.
- **Supabase (PostgreSQL)**: Database backend.
- **supabase-py**: Official Python client for Supabase.
- **Pydantic**: Data validation and settings management.
- **JWT Authentication**: Role-based access control.
- **Python 3.10+**

## 👤 Features

### 🔐 Authentication & Authorization
- Manual JWT authentication using `passlib` & `bcrypt`.
- Login endpoint and protected routes via Bearer token.
- **Role-based Access Control (RBAC):**
  - `ADMIN`: Full access (create, read, update, delete).
  - `ANALYST`: Manage financial records (create, read, update).
  - `VIEWER`: Read-only access to records and dashboards.

### 💰 Financial Records
Endpoints to manage income/expense records with role constraints. Features include filters by date range, category, and type.

### 📊 Dashboard
Aggregated analytics endpoints:
- Total income, expenses, and net balance.
- Summary broken down by category.
- Recent transactions list.
- Daily financial trends.

## 🚀 Setup Instructions

1. Clone the repository and navigate explicitly into this directory.
2. Create and activate a Python virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root configuration directory and add:
   ```env
   PROJECT_NAME="Finance Data Processing API"
   SUPABASE_URL="https://your-project-url.supabase.co"
   SUPABASE_KEY="your-anon-or-service-role-key"
   SECRET_KEY="your-randomly-generated-secret-key"
   ```
5. Run the FastAPI development server:
   ```powershell
   uvicorn app.main:app --reload
   ```

## 🧪 Testing

1. Navigate to the automatically generated Swagger UI at: `http://127.0.0.1:8000/docs`.
2. Register a new user at `POST /auth/register` supplying a role (`ADMIN`, `ANALYST`, or `VIEWER`).
3. Obtain an access token at `POST /auth/login`.
4. Click the **Authorize** lock button in the top right to paste the token and authenticate future API requests.