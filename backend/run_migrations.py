import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Running database migrations for Users, Sessions, and ChatMessages...")
    
    # 1. Create extension if possible
    try:
        db.session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Note: uuid-ossp extension:", e)

    # 2. Users Table
    db.session.execute(text("""
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
    db.session.commit()
    print("Users table ready.")

    # 3. Sessions Table
    db.session.execute(text("""
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
    db.session.commit()
    print("Sessions table ready.")

    # 4. Modify chat_messages Table columns
    # Add document_id, user_id, confidence, sources
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
            db.session.execute(text(q))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Notice on '{q}': {e}")

    # 5. Create Indexes
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);",
        "CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_doc ON chat_messages(document_id, created_at ASC);",
        "CREATE INDEX IF NOT EXISTS idx_chat_messages_user ON chat_messages(user_id, created_at ASC);"
    ]
    for idx_sql in indexes:
        try:
            db.session.execute(text(idx_sql))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Notice on index: {e}")

    print("All database migrations completed successfully!")
