import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db, Base

# --- Test Database Setup ---
# This test suite expects a PostgreSQL database to be running on localhost:5433,
# which can be started with `docker-compose up -d`.
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5433/linkzipdb"

@pytest.fixture(scope="session")
def test_db_engine():
    return create_engine(SQLALCHEMY_DATABASE_URL)

@pytest.fixture(scope="function")
def dbsession(test_db_engine):
    """Yield a new database session for a test, and rollback any changes."""
    connection = test_db_engine.connect()
    trans = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    # Create all tables for the test
    Base.metadata.create_all(bind=connection)

    yield session

    # Rollback and close the session
    session.close()
    trans.rollback()
    connection.close()

    # Drop all tables after the test
    Base.metadata.drop_all(bind=test_db_engine)

@pytest.fixture(scope="function")
def client(dbsession):
    """Yield a test client that uses the test database session."""
    def override_get_db():
        yield dbsession

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    del app.dependency_overrides[get_db]


# === Test Cases (No changes needed) ===

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
    create_response = client.post("/api/urls", json={"original_url": "https://www.example.com"})
    short_key = create_response.json()["short_key"]

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
