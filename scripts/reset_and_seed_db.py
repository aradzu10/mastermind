"""
Script to reset the database and seed it with AI players.

This script will:
1. Drop all tables from the database
2. Run alembic migrations to recreate the schema
3. Seed the database with hardcoded AI users
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.core.ai import AradzBot, RandomAI

# Database URL - you can override this with an environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://mastermind:mastermind_dev@localhost:5432/mastermind")

# Hardcoded AI users
AI_USERS = [
    AradzBot.user(),
    RandomAI.user(),
]


async def drop_all_tables(engine):
    """Drop all tables in the database."""
    print("Dropping all tables...")
    async with engine.begin() as conn:
        # Drop all tables
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO mastermind"))
        await conn.execute(text("GRANT ALL ON SCHEMA public TO public"))
    print("✓ All tables dropped")


async def run_migrations():
    """Run alembic migrations."""
    print("\nRunning alembic migrations...")
    import subprocess

    result = subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Migration failed: {result.stderr}")
        sys.exit(1)
    print("✓ Migrations completed")


async def seed_ai_users(session: AsyncSession):
    """Seed the database with AI users."""
    print("\nSeeding AI users...")

    created_users = []
    for ai_data in AI_USERS:
        session.add(ai_data)
        created_users.append(ai_data)

    await session.commit()

    print("✓ AI users created:")
    for user in created_users:
        await session.refresh(user)
        print(f"  - {user.display_name} (ID: {user.id}, Email: {user.email}, ELO: {user.elo_rating})")

    return created_users


async def main():
    """Main function to reset and seed the database."""
    print("=" * 60)
    print("Database Reset and Seed Script")
    print("=" * 60)
    print(f"\nDatabase URL: {DATABASE_URL}\n")

    # Create engine
    engine = create_async_engine(DATABASE_URL, echo=False)

    try:
        # Step 1: Drop all tables
        await drop_all_tables(engine)

        # Step 2: Run migrations
        await run_migrations()

        # Step 3: Seed AI users
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            users = await seed_ai_users(session)

        print("\n" + "=" * 60)
        print("✓ Database reset and seeding completed successfully!")
        print("=" * 60)
        print("\nAI User IDs for reference:")
        for user in users:
            print(f"  {user.display_name}: {user.id}")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
