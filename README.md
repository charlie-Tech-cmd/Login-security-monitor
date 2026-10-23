# Login Security Monitor

A full-stack authentication application built with FastAPI and PostgreSQL on the backend and React on the frontend. The project demonstrates secure user registration, persistent database storage, Argon2id password hashing, JWT-based session handling, and login attempt monitoring with temporary lockout protection.

## Overview

This application includes:

- User registration with client and server password validation
- Persistent user storage using PostgreSQL and SQLAlchemy
- Secure password hashing using Argon2id
- JWT-based authentication for protected API routes
- Login lockout protection after repeated failed attempts
- React frontend with sign-up, sign-in, and guarded dashboard access
- Development reverse proxy and flexible CORS configuration

## Tech Stack

### Backend
- **Python 3.12+**
- **FastAPI**: RESTful API framework
- **SQLAlchemy 2.0+**: ORM and database engine
- **PostgreSQL**: Relational database storage
- **psycopg2-binary**: PostgreSQL database adapter
- **Pydantic & Pydantic-Settings**: Data validation and environment settings
- **Argon2-cffi**: Modern password hashing (Argon2id)
- **PyJWT**: JSON Web Token encoding and decoding
- **Uvicorn**: ASGI web server

### Frontend
- **React 18**: UI component library
- **Vite 6**: Frontend tooling and development server (with built-in API proxy)
- **React Router 7**: Client-side routing and protected routes
- **Tailwind CSS 4**: Modern styling

---

## Project Structure

```text
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   └── auth.py             # Auth endpoints (/register, /login, /me)
│   │   │   ├── dependencies.py         # JWT bearer authentication dependency
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py               # Pydantic settings & DB URL assembly
│   │   │   ├── database.py             # SQLAlchemy engine & session factory
│   │   │   ├── jwt.py                  # Token creation & verification
│   │   │   ├── security.py             # Argon2 password hashing & verification
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── user.py                 # SQLAlchemy UserModel (users table)
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── auth.py                 # Pydantic request/response schemas
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── auth_service.py         # Auth business logic
│   │   │   ├── login_monitor.py        # Failed login tracking & lockout
│   │   │   ├── user_store.py           # PostgresUserStore & InMemoryUserStore
│   │   │   └── __init__.py
│   │   ├── main.py                     # FastAPI application & startup lifespan
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_auth.py                # Core authentication tests
│   │   ├── test_auth_routes.py         # FastAPI route tests
│   │   ├── test_auth_service.py        # AuthService logic tests
│   │   ├── test_jwt.py                 # JWT token creation & expiry tests
│   │   ├── test_login_monitor.py       # Lockout tracking tests
│   │   └── test_postgres_store.py      # PostgreSQL persistence & CRUD tests
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Backend environment variables template
│   └── .env                            # Backend environment variables (git-ignored)
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AuthLayout.jsx          # Shared container layout
│   │   │   └── PasswordField.jsx       # Password input with strength checklist
│   │   ├── pages/
│   │   │   ├── HomePage.jsx            # Guarded dashboard page
│   │   │   ├── LoginPage.jsx           # Sign-in page
│   │   │   └── RegisterPage.jsx        # Account registration page
│   │   ├── services/
│   │   │   └── authService.js          # API client & token storage
│   │   ├── utils/
│   │   │   └── validation.js           # Password requirements & email regex
│   │   ├── App.jsx                     # Route definitions & ProtectedRoute guard
│   │   ├── main.jsx                    # React application entry point
│   │   └── styles.css                  # Global styles & Tailwind import
│   ├── tests/
│   │   └── validation.test.js          # Frontend validation unit tests
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js                  # Vite configuration & /api proxy
│   └── README.md
└── README.md
```

---

## Features

### Authentication API
The backend exposes authentication routes under `/api/auth`:

- `POST /api/auth/register` - Validate and persist a new user in PostgreSQL (returns HTTP 201).
- `POST /api/auth/login` - Verify credentials against stored Argon2id hash and return a signed JWT.
- `GET /api/auth/me` - Return the current authenticated user from the database via Bearer token.

### Security Features
- **Argon2id Hashing**: Passwords are securely hashed with Argon2id before storage.
- **Persistent Storage**: User credentials and timestamps are stored in a relational PostgreSQL database.
- **Lockout Protection**: Failed login attempts are monitored; 5 consecutive failures temporarily lock the account.
- **Informative Error Messages**: Lockout states return explicit notifications (`"Too many failed login attempts. Please try again later."`) rather than masking the lockout as bad credentials.
- **RFC 7518 Compliant JWTs**: Tokens are signed using HMAC-SHA256 with a 32+ byte cryptographic secret key.

### Frontend Features
- **Live Password Strength Meter**: Visual indicator tracking 5 requirements (length, uppercase, lowercase, numbers, special characters).
- **Client & Server Validation**: Catches malformed inputs and parses structured FastAPI HTTP 422 error arrays.
- **Protected Routing**: Guarded `/home` dashboard route that automatically redirects to `/login` when unauthorized.
- **Vite Proxy**: Pre-configured reverse proxy routing `/api` requests to `http://127.0.0.1:8000`.

---

## Configuration

### Backend Environment (`backend/.env`)

The backend reads configuration using Pydantic Settings. Individual PostgreSQL connection parameters are configured separately and assembled dynamically:

```env
# JWT Secret Key (minimum 32 bytes for HMAC-SHA256)
JWT_SECRET_KEY=change-this-secret-key-with-at-least-32-bytes!

# PostgreSQL Configuration
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=login_security_monitor

# Optional: Full URL override (takes precedence if defined)
# DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/login_security_monitor
```

> **Note on `POSTGRES_HOST`**: 
> - For standard installations, TablePlus, and GUI tools, use `localhost` or `127.0.0.1`.
> - If running inside a sandboxed Linux environment where network loopback is restricted, set `POSTGRES_HOST=/tmp` to connect via Unix domain socket.

### Frontend Environment (`frontend/.env.local` - Optional)

The frontend uses Vite's proxy by default. To point to an external backend host directly, copy `.env.example` to `.env.local`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd Login-security-monitor
```

### 2. Set up Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Ensure `backend/.env` is configured with your database credentials and secret key.

### 3. Set up Frontend

Open a new terminal window:

```bash
cd frontend
npm install
```

---

## Running the Application

### 1. Start the Backend

From the `backend` directory with the virtual environment activated:

```bash
cd backend
uvicorn app.main:app --reload
```

The API will run on `http://127.0.0.1:8000`. Database tables are automatically initialized on startup via FastAPI's lifespan handler.

Health check:
```bash
curl http://127.0.0.1:8000/health
```

### 2. Start the Frontend

From the `frontend` directory:

```bash
cd frontend
npm run dev
```

The React application will run with Vite on `http://localhost:5173`.

---

## Database Inspection

You can connect to the database using GUI clients such as **TablePlus** or the **VS Code PostgreSQL Extension**:

- **Host**: `localhost` (or `127.0.0.1`)
- **Port**: `5432`
- **User**: value of `POSTGRES_USER` (e.g. `postgres`)
- **Password**: value of `POSTGRES_PASSWORD`
- **Database**: value of `POSTGRES_DB` (e.g. `login_security_monitor`)
- **Table**: `users`

---

## Testing

### Backend Tests
Run the complete backend test suite (46 tests covering authentication, routes, lockout monitor, and PostgreSQL persistence):

```bash
cd backend
pytest tests
```

### Frontend Tests & Build
Run the frontend validation tests and production build:

```bash
cd frontend
npm test
npm run build
```

---

## License

This project does not include a specific license file in the workspace; usage and distribution follow the requirements of the owning organization.
