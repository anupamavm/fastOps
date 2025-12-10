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

## Improvements for Industry Standards

### 1. Database Migrations

**Current:** Using `Base.metadata.create_all()` - only creates missing tables, can't modify existing schema

**Industry Standard:**

- ✅ Use Alembic for version-controlled migrations
- ✅ Track schema changes in version control
- ✅ Support rollback capability
- ✅ Handle complex schema changes (renames, type changes, etc.)

```powershell
# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### 2. Configuration Management

**Current:** Using `os.getenv()` with `.env` file

**Industry Standard:**

- ✅ Use Pydantic Settings for type-safe configuration
- ✅ Support multiple environments (dev, staging, prod)
- ✅ Validate environment variables at startup
- ✅ Use secrets management (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    groq_api_key: str
    environment: str = "development"

    class Config:
        env_file = ".env"
```

### 3. Logging & Monitoring

**Current:** No structured logging

**Industry Standard:**

- ✅ Structured logging (JSON format)
- ✅ Request/response logging middleware
- ✅ Correlation IDs for request tracing
- ✅ Integration with monitoring tools (Datadog, New Relic, Prometheus)
- ✅ Error tracking (Sentry, Rollbar)

```python
import logging
import structlog

logger = structlog.get_logger()
logger.info("user_created", user_id=user.id, email=user.email)
```

### 4. Testing

**Current:** pytest installed but no tests

**Industry Standard:**

- ✅ Unit tests for services and models
- ✅ Integration tests for API endpoints
- ✅ Test coverage reporting (aim for 80%+)
- ✅ Automated testing in CI/CD pipeline
- ✅ Mock external dependencies (database, LLM APIs)

```python
# tests/test_user_service.py
def test_create_user(db_session):
    user = create_user(db_session, UserCreate(name="Test", email="test@test.com"))
    assert user.name == "Test"
```

### 5. API Documentation

**Current:** Auto-generated Swagger docs

**Industry Standard:**

- ✅ Add detailed descriptions and examples to endpoints
- ✅ Document response models and error codes
- ✅ Include authentication/authorization info
- ✅ Add request/response examples
- ✅ Version your API (e.g., `/api/v1/users`)

```python
@router.post("/", response_model=User, status_code=201,
    summary="Create a new user",
    description="Creates a new user with the provided information",
    responses={
        409: {"description": "User already exists"},
        422: {"description": "Validation error"}
    })
```

### 6. Error Handling

**Current:** Default FastAPI error handling

**Industry Standard:**

- ✅ Custom exception hierarchy
- ✅ Consistent error response format
- ✅ Global exception handlers
- ✅ Proper HTTP status codes
- ✅ Don't expose internal errors to clients

```python
class APIException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(APIException)
async def api_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
```

### 7. Authentication & Authorization

**Current:** No authentication implemented

**Industry Standard:**

- ✅ JWT tokens with refresh mechanism
- ✅ OAuth2/OIDC integration
- ✅ Role-based access control (RBAC)
- ✅ API key authentication for service-to-service
- ✅ Rate limiting per user/API key

```python
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

@router.get("/protected")
async def protected_route(token: str = Depends(security)):
    payload = jwt.decode(token, SECRET_KEY)
    return {"user_id": payload["sub"]}
```

### 8. Database Connection Management

**Current:** Creating new session for each request

**Industry Standard:**

- ✅ Connection pooling with proper limits
- ✅ Connection health checks
- ✅ Automatic retry on transient failures
- ✅ Read replicas for read-heavy workloads
- ✅ Database connection monitoring

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Health check
    pool_recycle=3600    # Recycle connections
)
```

### 9. Async/Performance

**Current:** Synchronous database operations

**Industry Standard:**

- ✅ Use async database drivers (asyncpg, aiomysql)
- ✅ Async SQLAlchemy for non-blocking I/O
- ✅ Background tasks for heavy operations (Celery, RQ)
- ✅ Caching layer (Redis) for frequently accessed data
- ✅ Database query optimization and indexing

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

engine = create_async_engine("postgresql+asyncpg://...")

async def get_user(user_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
```

### 10. Security Best Practices

**Current:** Basic setup

**Industry Standard:**

- ✅ HTTPS only (enforce in production)
- ✅ CORS configuration for frontend integration
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (parameterized queries)
- ✅ Rate limiting and throttling
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ Dependency vulnerability scanning (Snyk, Dependabot)
- ✅ Secrets rotation policy

```python
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### 11. CI/CD Pipeline

**Current:** Manual deployment

**Industry Standard:**

- ✅ GitHub Actions / GitLab CI for automated testing
- ✅ Automated code quality checks (linting, type checking)
- ✅ Automated security scanning
- ✅ Automated deployments to staging/production
- ✅ Database migration automation
- ✅ Blue-green or canary deployments
- ✅ Automated rollback on failure

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: pytest --cov=app tests/
      - name: Lint
        run: flake8 app/
```

### 12. Documentation

**Current:** Basic README

**Industry Standard:**

- ✅ Comprehensive API documentation
- ✅ Architecture decision records (ADRs)
- ✅ Deployment guide
- ✅ Troubleshooting guide
- ✅ Code comments for complex logic
- ✅ OpenAPI/Swagger specs
- ✅ Changelog for version tracking

### 13. Vector Database (RAG)

**Current:** In-memory FAISS or basic pgvector

**Industry Standard:**

- ✅ Dedicated vector databases (Pinecone, Weaviate, Qdrant)
- ✅ Vector index optimization (HNSW, IVF)
- ✅ Batch embedding generation
- ✅ Metadata filtering on vector search
- ✅ Hybrid search (vector + keyword)
- ✅ Vector similarity caching

### 14. Observability

**Current:** No observability

**Industry Standard:**

- ✅ Distributed tracing (OpenTelemetry, Jaeger)
- ✅ Metrics collection (request rate, latency, errors)
- ✅ Custom business metrics
- ✅ Alerting on anomalies
- ✅ Dashboard for real-time monitoring
- ✅ APM tools (Application Performance Monitoring)

### 15. Data Validation & Quality

**Current:** Basic Pydantic validation

**Industry Standard:**

- ✅ Input sanitization for XSS prevention
- ✅ Custom validators for business rules
- ✅ Schema evolution strategy
- ✅ Data quality monitoring
- ✅ Audit logging for data changes

---

## Priority Implementation Order

1. **Database Migrations** (Alembic) - Foundation for schema management
2. **Testing** - Ensure code quality and prevent regressions
3. **Configuration Management** - Type-safe, environment-aware config
4. **Logging** - Visibility into application behavior
5. **Error Handling** - Better user experience and debugging
6. **Authentication** - Security basics
7. **CI/CD** - Automation and reliability
8. **Monitoring** - Production readiness
9. **Performance Optimization** - Scale and efficiency
10. **Advanced Features** - Enhanced capabilities
