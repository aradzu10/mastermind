"""add_starter_id_to_single_games

Revision ID: 34396aeabad9
Revises: 366e6e759667
Create Date: 2026-01-18 13:44:14.185710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34396aeabad9'
down_revision: Union[str, Sequence[str], None] = '366e6e759667'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add starter_id column to single_games table
    op.add_column('single_games', sa.Column('starter_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_single_games_starter_id', 'single_games', 'users', ['starter_id'], ['id'])
    
    # Populate starter_id with player_id for existing single-player games
    op.execute("""
        UPDATE single_games 
        SET starter_id = player1_id
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key and column
    op.drop_constraint('fk_single_games_starter_id', 'single_games', type_='foreignkey')
    op.drop_column('single_games', 'starter_id')
