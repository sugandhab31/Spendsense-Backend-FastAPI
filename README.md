# Spendsense Backend (FastAPI)

Spendsense is a personal expense tracking application. This is the backend built using FastAPI and PostgreSQL.

## 🚀 Features

- User registration and authentication
- CRUD operations for expenses
- Expense categorization
- Monthly expense summaries

## 🛠️ Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (for DB migrations)
- Pydantic
- Uvicorn

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/sugandhab31/Spendsense-Backend-FastAPI.git
cd Spendsense-Backend-FastAPI

Create a virtual environment

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Run the APP
uvicorn main:app --reload
