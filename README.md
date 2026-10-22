# Login Security Monitor

A full-stack authentication application built with FastAPI on the backend and React on the frontend. The project demonstrates secure user registration, password hashing, JWT-based session handling, and login attempt monitoring with temporary lockout protection.

## Overview

This application includes:

- User registration with password validation
- Secure password hashing using Argon2id
- JWT-based authentication for protected API routes
- Login lockout protection after repeated failed attempts
- React frontend for sign-up, sign-in, and protected home access
- In-memory user storage for local development and testing

## Tech Stack

### Backend
- Python
- FastAPI
- Pydantic
- Argon2-cffi
- PyJWT
- Uvicorn

### Frontend
- React
- Vite
- React Router

## Project Structure

```text
.
├── app/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   │       └── auth.py
│   ├── core/
│   │   ├── config.py
│   │   ├── jwt.py
│   │   └── security.py
│   ├── main.py
│   ├── schemas/
│   │   └── auth.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── login_monitor.py
│   │   └── user_store.py
│   └── __init__.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   ├── README.md
│   ├── vite.config.js
│   └── tests/
├── tests/
│   ├── test_auth.py
│   ├── test_auth_routes.py
│   ├── test_auth_service.py
│   ├── test_jwt.py
│   └── test_login_monitor.py
├── requirements.txt
└── README.md
```

## Features

### Authentication API
The backend exposes authentication routes under `/api/auth`:

- `POST /api/auth/register` - create a new user account
- `POST /api/auth/login` - authenticate and return a JWT
- `GET /api/auth/me` - return the current authenticated user

### Security Features
- Passwords are hashed with Argon2id before storage
- Minimum password length is enforced
- JWTs are signed with a configurable secret key
- Failed login attempts are tracked in memory
- Accounts are temporarily locked after repeated failures within a configured time window

### Frontend
The frontend includes:

- Registration page
- Login page
- Protected route guard for authenticated users
- Home page shown after successful sign-in
- Token storage in sessionStorage for browser sessions

## Configuration

The backend reads configuration from `.env` using Pydantic settings. A minimal example is:

```env
JWT_SECRET_KEY=your-super-secret-key
```

The project also includes defaults for:

- app name: `Login Security Monitor`
- password minimum length: `8`
- CORS origins for local frontend development
- failed login threshold: `5` attempts
- failure window: `15` minutes
- lockout duration: `15` minutes
- JWT expiration: `15` minutes

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Login-security-monitor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file in the project root:

```env
JWT_SECRET_KEY=change-this-secret-key
```

## Running the Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will typically run on:

```text
http://127.0.0.1:8000
```

Health check endpoint:

```bash
curl http://127.0.0.1:8000/health
```

## Running the Frontend

Open a separate terminal and run:

```bash
cd frontend
npm install
npm run dev
```

The React app will run with Vite, typically on:

```text
http://localhost:5173
```

## Example Authentication Flow

1. Register a user through the frontend or API
2. Log in with the same credentials
3. Receive an access token in the response
4. Use the token in the `Authorization: Bearer <token>` header for protected requests
5. Access the guarded home page after successful authentication

## Notes

This project uses an in-memory user store and in-memory login monitor, which is ideal for local development and testing. Restarting the backend will reset stored users and failed-login tracking.

## Testing

The repository includes pytest-based tests for authentication behavior, JWT logic, and login monitoring.

Run tests with:

```bash
pytest
```

## License

This project does not include a specific license file in the workspace, so usage and distribution should follow the requirements of the owning repository or organization.
