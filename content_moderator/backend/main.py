import sqlalchemy
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
import hashlib
import secrets
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from schemas import *
from database import engine, async_session,get_db

load_dotenv()

API_KEY_NAME = os.getenv("API_KEY")


def _api_key_generator(prefix: str = "sk_live_") -> tuple[str, str]:
    """Generates a raw key for the user and its SHA-256 hash for the DB."""
    raw_secret = secrets.token_hex(32)
    full_key = f"{prefix}{raw_secret}"
    hashed_key = hashlib.sha256(full_key.encode()).hexdigest()
    return full_key, hashed_key

def _key_provider(key: str) -> str:
    """Hashes an incoming API key to compare with the database."""
    return hashlib.sha256(key.encode()).hexdigest()

app = FastAPI(title='Content Moderator')
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

@app.post("/developer/keys", response_model=KeyResponse)
async def create_new_api_key(payload: KeyCreate, db: AsyncSession = Depends(get_db)):
    plain_key, hashed_key = _api_key_generator()

    expiration = None
    if payload.expires_in_days:
        expiration = datetime.utcnow() + timedelta(days=payload.expires_in_days)
    
    db_key = Api_model(
        user_id=payload.user_id,
        key_prefix=plain_key[:12], 
        hashed_key=hashed_key,
        name=payload.name,
        expires_at=expiration
    )
    db.add(db_key)
    await db.commit()
    return KeyResponse(name=db_key.name, plain_text_key=plain_key)

@app.get('/v1/ingest')
def ingest(Ingest_input):
    return 'data stored Successfully'


@app.post('/v1/text_review')
def text_review(Ingest_input):
    return 'True'


@app.post('/v1/Image_review')
def image_review(Ingest_input):
    return 'False'

