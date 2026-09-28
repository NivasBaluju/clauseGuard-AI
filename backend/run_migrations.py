import os
import sys
from pathlib import Path
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent / ".env")
except Exception:
    pass

from sqlalchemy import create_engine, text

raw_db_url = os.environ.get("DATABASE_URL")

if not raw_db_url:
    print("CRITICAL ERROR: DATABASE_URL environment variable is not set!")
    print("Please configure DATABASE_URL in the Railway 'Variables' tab.")
    sys.exit(1)

if raw_db_url.startswith("postgres://"):
    raw_db_url = raw_db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif raw_db_url.startswith("postgresql://"):
    raw_db_url = raw_db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

try:
    clean_url = raw_db_url.replace("postgresql+psycopg2://", "http://").replace("postgresql://", "http://")
    parsed = urlparse(clean_url)
    print(f"Connecting to database host: {parsed.hostname}...")
except Exception:
    print("Connecting to database...")

try:
    engine = create_engine(raw_db_url, pool_pre_ping=True)
    with engine.begin() as conn:
        print("Running database migrations for Users, Sessions, and ChatMessages...")

        try:
            conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        except Exception as e:
            print("Note: uuid-ossp extension:", e)

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'user',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """))
        print("Users table ready.")

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS sessions (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            device_fingerprint VARCHAR(255),
            ip VARCHAR(64),
            revoked BOOLEAN DEFAULT false,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        );
        """))
        print("Sessions table ready.")

        cols_to_add = [
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS document_id UUID REFERENCES documents(id) ON DELETE SET NULL;",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS user_id UUID REFERENCES users(id) ON DELETE CASCADE;",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS confidence DOUBLE PRECISION;",
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS sources JSONB DEFAULT '[]'::jsonb;",
            "ALTER TABLE chat_messages ALTER COLUMN session_id DROP NOT NULL;",
            "ALTER TABLE chat_messages ALTER COLUMN role TYPE VARCHAR(20);"
        ]
        for q in cols_to_add:
            try:
                conn.execute(text(q))
            except Exception as e:
                print(f"Notice on column migration: {e}")

        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
            "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_chat_messages_doc ON chat_messages(document_id, created_at ASC);",
            "CREATE INDEX IF NOT EXISTS idx_chat_messages_user ON chat_messages(user_id, created_at ASC);"
        ]
        for idx_sql in indexes:
            try:
                conn.execute(text(idx_sql))
            except Exception as e:
                print(f"Notice on index: {e}")

        print("All database migrations completed successfully!")

except Exception as err:
    print(f"Database migration failed: {err}")
    sys.exit(1)
