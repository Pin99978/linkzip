import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db, Base

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_temp.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Dependency Override for Testing ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Tell the app to use our test DB instead of the real one
app.dependency_overrides[get_db] = override_get_db

# --- Test Client Setup ---
@pytest.fixture(scope="function")
def client():
    # Create tables for each test function
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    # Drop tables after each test function
    Base.metadata.drop_all(bind=engine)

# === Test Cases ===

def test_create_short_url_success(client):
    """Test creating a short URL successfully."""
    response = client.post(
        "/api/urls",
        json={"original_url": "https://www.google.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["original_url"] == "https://www.google.com"
    assert "short_key" in data
    assert len(data["short_key"]) == 6

def test_create_short_url_invalid_format(client):
    """Test creating a short URL with an invalid URL format."""
    response = client.post(
        "/api/urls",
        json={"original_url": "not_a_url"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid URL format. Must start with http:// or https://"}

def test_redirect_to_original_url_success(client):
    """Test redirection with a valid short key."""
    # First, create a URL
    create_response = client.post("/api/urls", json={"original_url": "https://www.example.com"})
    short_key = create_response.json()["short_key"]

    # Then, test redirection (follow_redirects=False is crucial to inspect the 307 response)
    redirect_response = client.get(f"/{short_key}", follow_redirects=False)
    assert redirect_response.status_code == 307
    assert redirect_response.headers["location"] == "https://www.example.com"

def test_redirect_to_original_url_not_found(client):
    """Test redirection with a non-existent short key."""
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == 404

def test_get_url_info_success(client):
    """Test getting info for a valid short key."""
    create_response = client.post("/api/urls", json={"original_url": "https://www.github.com"})
    short_key = create_response.json()["short_key"]

    info_response = client.get(f"/api/info/{short_key}")
    assert info_response.status_code == 200
    data = info_response.json()
    assert data["original_url"] == "https://www.github.com"
    assert data["short_key"] == short_key

def test_get_url_info_not_found(client):
    """Test getting info for a non-existent short key."""
    response = client.get("/api/info/nonexistent")
    assert response.status_code == 404
