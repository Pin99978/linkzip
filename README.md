# LinkZip 🔗

A simple, fast, and modern URL shortener built with FastAPI and React.

LinkZip is a demonstration project showcasing a full-stack application with a Python backend, a React frontend, and a containerized deployment workflow using Docker.

## ✨ Features

- **Create Short URLs**: Convert long URLs into a 6-character short key.
- **Redirection**: Automatically redirects short URLs to their original destination.
- **API-First Design**: A clean, documented API for creating and retrieving URL information.
- **Containerized**: Comes with a `Dockerfile` for easy and consistent deployment.
- **Fully Tested**: Backend API is covered by a full suite of automated tests using `pytest`.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, Uvicorn
- **Frontend**: JavaScript, React
- **Database**: SQLite (for simplicity)
- **Testing**: Pytest, HTTPX
- **Deployment**: Docker

## 🚀 Getting Started (Local Development)

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.10+
- Node.js v16+ and npm
- A virtual environment tool for Python (e.g., `venv`)

### 1. Backend Setup

First, set up and run the FastAPI backend server.

```bash
# 1. Clone the repository (if you haven't already)
# git clone <repository-url>
# cd linkzip

# 2. Create and activate a Python virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install backend dependencies
pip install -r requirements.txt

# 4. Run the backend server
# The --reload flag will automatically restart the server on code changes.
uvicorn src.main:app --reload
```

Your backend API is now running on `http://127.0.0.1:8000`.

### 2. Frontend Setup

In a **new, separate terminal**, set up and run the React frontend.

```bash
# 1. Navigate to the frontend directory
cd frontend

# 2. Install frontend dependencies
npm install

# 3. Start the React development server
npm start
```

Your browser should automatically open to `http://localhost:3000`, where you can interact with the LinkZip web interface.

## ✅ Running Tests

To ensure everything is working correctly, you can run the backend test suite.

First, install the testing dependencies:
```bash
pip install pytest httpx
```

Then, from the **project root directory**, run pytest:
```bash
pytest
```

## 🐳 Running with Docker

Once you have Docker installed, you can build and run the backend service as a container.

```bash
# 1. Build the Docker image
docker build -t linkzip-backend .

# 2. Run the container
# This maps port 8000 of your machine to port 8000 inside the container.
docker run -p 8000:8000 linkzip-backend
```
