# FastOps API

A FastAPI application with a clean layered architecture.

## Project Structure

```
fastOps/
├── app/
│   ├── __init__.py
│   ├── config/          # Configuration and database setup
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models/          # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/         # Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── services/        # Business logic
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── routers/         # API endpoints
│       ├── __init__.py
│       └── user.py
├── main.py              # Application entry point
├── .env                 # Environment variables
├── requirements.txt     # Dependencies
└── README.md
```

## Layers

- **config/**: Database configuration and connection management
- **models/**: Database models (SQLAlchemy ORM)
- **schemas/**: Request/Response schemas (Pydantic)
- **services/**: Business logic and data operations
- **routers/**: API route handlers

## Running the Application

1. Activate virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the server:

```powershell
uvicorn main:app --reload
```

4. Access the API documentation:
   - Swagger UI: http://127.0.0.1:8000/docs
   - ReDoc: http://127.0.0.1:8000/redoc

## Environment Variables

Create a `.env` file with:

```
DATABASE_URL=sqlite:///./fastops.db
```

For PostgreSQL:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```
