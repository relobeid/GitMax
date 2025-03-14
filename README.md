# GitMax - GitHub Career Coaching Platform

A platform that helps developers assess their GitHub profile against job requirements.

## Features

- GitHub OAuth authentication
- GitHub profile analysis
- Profile scoring based on job roles
- Personalized recommendations

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- GitHub OAuth App credentials

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/gitmax.git
   cd gitmax
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your GitHub OAuth App:
   - Go to GitHub Developer Settings > OAuth Apps > New OAuth App
   - Set the callback URL to `http://localhost:8000/api/auth/callback`
   - Copy the Client ID and Client Secret

5. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values with your GitHub OAuth credentials and PostgreSQL connection string

6. Set up the PostgreSQL database:
   - Create a database named `gitmax`
   - The tables will be created automatically when you run the application

### Running the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

API documentation is available at `http://localhost:8000/docs`.

## API Endpoints

- `GET /api/auth/login`: Redirects to GitHub OAuth login
- `GET /api/auth/callback`: GitHub OAuth callback
- `GET /api/profile`: Get authenticated user's profile data

## Project Structure

```
app/
├── __init__.py
├── main.py           # FastAPI application entry point
├── database.py       # Database connection and models
├── auth.py           # Authentication utilities
├── models/           # Pydantic models
│   ├── __init__.py
│   └── user.py
├── routers/          # API routes
│   ├── __init__.py
│   ├── auth.py
│   └── profile.py
├── services/         # Business logic
│   ├── __init__.py
│   └── github.py
└── utils/            # Utility functions
    ├── __init__.py
    └── config.py
```