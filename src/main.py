from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime, UTC
import random
import string
import os
from fastapi.staticfiles import StaticFiles

# --- Database Setup ---
# Use environment variable for production, fallback to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL)

# Add a check for SQLite to handle connect_args
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- SQLAlchemy Model ---
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

# Create the database tables
Base.metadata.create_all(bind=engine)

# --- Pydantic Models ---
class URLBase(BaseModel):
    original_url: str

class URLInfo(URLBase):
    short_key: str
    model_config = ConfigDict(from_attributes=True)

# --- FastAPI App ---
app = FastAPI(
    title="LinkZip API",
    description="A simple URL shortener API.",
    version="0.1.0"
)

# --- Helper Functions ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_key(db_session: Session) -> str:
    """Generate a unique short key."""
    while True:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not db_session.query(URL).filter(URL.short_key == key).first():
            return key

# --- API Endpoints ---
@app.post("/api/urls", response_model=URLInfo, status_code=201)
def create_short_url(url: URLBase, db: Session = Depends(get_db)):
    """
    Create a new short URL.
    """
    if not (url.original_url.startswith("http://") or url.original_url.startswith("https://")):
        raise HTTPException(status_code=400, detail="Invalid URL format. Must start with http:// or https://")

    short_key = generate_short_key(db)
    db_url = URL(original_url=url.original_url, short_key=short_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

@app.get("/{short_key}")
def redirect_to_original_url(short_key: str, db: Session = Depends(get_db)):
    """
    Redirects to the original URL associated with the short key.
    """
    db_url = db.query(URL).filter(URL.short_key == short_key).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return RedirectResponse(url=db_url.original_url)

@app.get("/api/info/{short_key}", response_model=URLInfo)
def get_url_info(short_key: str, db: Session = Depends(get_db)):
    """
    Get information about a short URL.
    """
    db_url = db.query(URL).filter(URL.short_key == short_key).first()
    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    return db_url

# --- Mount Static Files (Frontend) ---
# This must be after all API routes
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")
