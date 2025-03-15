# GitMax - GitHub-based Career Coaching Platform

GitMax is a platform that helps developers assess their GitHub profile against job requirements. It analyzes repositories, commits, and tech stacks to generate a profile score and provide personalized recommendations.

## Features

- **GitHub OAuth Authentication**: Connect your GitHub profile securely
- **Profile Analysis**: Analyze repositories, commits, and tech stack
- **Profile Scoring**: Generate a score based on job roles
- **Personalized Recommendations**: Get tips to improve your profile
- **Modern UI**: Beautiful and responsive user interface built with React and Tailwind CSS

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: GitHub OAuth, JWT
- **API Client**: HTTPX

### Frontend
- **Framework**: React
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Routing**: React Router

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL
- GitHub OAuth App credentials

### Backend Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gitmax.git
cd gitmax
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set Up GitHub OAuth App

1. Go to GitHub Developer Settings: https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in the details:
   - Application name: GitMax (or your preferred name)
   - Homepage URL: http://localhost:8000
   - Authorization callback URL: http://localhost:8000/api/auth/callback
4. Register the application
5. Copy the Client ID and generate a Client Secret

#### 5. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```
# GitHub OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/callback

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gitmax

# JWT
SECRET_KEY=your_secret_key_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

Replace the placeholder values with your actual credentials.

#### 6. Create the Database

```bash
createdb gitmax
```

#### 7. Run the Backend Application

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000.

### Frontend Setup

#### 1. Navigate to the Frontend Directory

```bash
cd frontend-react
```

#### 2. Install Frontend Dependencies

```bash
npm install
```

#### 3. Run the Frontend Application

```bash
npm start
```

The frontend will be available at http://localhost:3000.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication Flow

1. User visits `/api/auth/login` → Redirected to GitHub
2. User authorizes the app → GitHub redirects to `/api/auth/callback`
3. Backend creates/updates user and sets JWT token in cookie
4. User is redirected to frontend with the token

## Project Structure

```
gitmax/
├── app/                # Backend application
│   ├── models/         # Pydantic models
│   ├── routers/        # API routes
│   ├── services/       # Business logic
│   ├── utils/          # Utility functions
│   ├── auth.py         # Authentication logic
│   ├── database.py     # Database connection and models
│   └── main.py         # Application entry point
├── frontend-react/     # Frontend application
│   ├── public/         # Static files
│   ├── src/            # Source code
│   │   ├── components/ # Reusable components
│   │   ├── pages/      # Page components
│   │   ├── App.js      # Main application component
│   │   └── index.js    # Entry point
│   ├── package.json    # Dependencies and scripts
│   └── tailwind.config.js # Tailwind CSS configuration
├── .env                # Environment variables
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

## Frontend Pages

- **Landing Page**: Introduction to GitMax with features and benefits
- **Login/Signup**: User authentication with GitHub OAuth
- **Dashboard**: Overview of GitHub profile with key metrics
- **Repository Analysis**: Detailed analysis of repositories with recommendations
- **Profile Scoring**: Profile score based on selected job role with strengths and weaknesses

## Next Steps

1. Connect frontend to backend API
2. Implement GitHub OAuth flow in the frontend
3. Fetch real GitHub data for analysis
4. Deploy the application to production

## License

MIT