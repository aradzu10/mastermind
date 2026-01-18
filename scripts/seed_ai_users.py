"""
Idempotent script to seed AI users into the database.

This script will check if AI users already exist and only insert them if they don't.
Safe to run multiple times - will skip if users already exist.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import from backend
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from backend.core.ai import AradzBot, RandomAI
from backend.db.models.user import User

# Database URL - you can override this with an environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://mastermind:mastermind_dev@localhost:5432/mastermind")

# Hardcoded AI users
AI_USERS = [
    AradzBot.user(),
    RandomAI.user(),
]


async def seed_ai_users(session: AsyncSession):
    """Seed the database with AI users if they don't already exist."""
    print("Checking for existing AI users...")

    # Check if AradzBot (id=0) already exists
    result = await session.execute(select(User).where(User.id == 0))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        print("✓ AI users already exist in database. Skipping seed.")
        return True

    print("Seeding AI users...")

    created_users = []
    for ai_data in AI_USERS:
        session.add(ai_data)
        created_users.append(ai_data)

    await session.commit()

    print("✓ AI users created successfully:")
    for user in created_users:
        await session.refresh(user)
        print(f"  - {user.display_name} (ID: {user.id}, Email: {user.email}, ELO: {user.elo_rating})")

    return True


async def main():
    """Main function to seed AI users."""
    print("=" * 60)
    print("AI Users Seed Script (Idempotent)")
    print("=" * 60)
    print(f"Database URL: {DATABASE_URL}\n")

    # Create engine
    engine = create_async_engine(DATABASE_URL, echo=False)

    try:
        # Seed AI users
        async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as session:
            success = await seed_ai_users(session)

        if success:
            print("\n" + "=" * 60)
            print("✓ AI users seed completed successfully!")
            print("=" * 60)
            sys.exit(0)
        else:
            print("\n✗ Failed to seed AI users")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
