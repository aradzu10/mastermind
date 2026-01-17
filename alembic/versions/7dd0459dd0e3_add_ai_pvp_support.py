"""add_ai_pvp_support

Revision ID: 7dd0459dd0e3
Revises: 7c2580e573cf
Create Date: 2026-01-16 19:55:11.028228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dd0459dd0e3'
down_revision: Union[str, Sequence[str], None] = '7c2580e573cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new columns to games table for AI mode
    op.add_column('games', sa.Column('player_secret', sa.String(length=4), nullable=True))
    op.add_column('games', sa.Column('ai_guesses', sa.JSON(), nullable=True))
    op.add_column('games', sa.Column('opponent_type', sa.String(), nullable=False, server_default='none'))
    
    # Create pvp_games table
    op.create_table(
        'pvp_games',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('player1_id', sa.Integer(), nullable=False),
        sa.Column('player2_id', sa.Integer(), nullable=True),
        sa.Column('player1_secret', sa.String(length=4), nullable=True),
        sa.Column('player2_secret', sa.String(length=4), nullable=True),
        sa.Column('player1_guesses', sa.JSON(), nullable=False),
        sa.Column('player2_guesses', sa.JSON(), nullable=False),
        sa.Column('current_turn', sa.Integer(), nullable=False),
        sa.Column('winner_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('started_at', sa.DateTime(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['player1_id'], ['users.id']),
        sa.ForeignKeyConstraint(['player2_id'], ['users.id']),
        sa.ForeignKeyConstraint(['winner_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pvp_games_id'), 'pvp_games', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Drop pvp_games table
    op.drop_index(op.f('ix_pvp_games_id'), table_name='pvp_games')
    op.drop_table('pvp_games')
    
    # Remove columns from games table
    op.drop_column('games', 'opponent_type')
    op.drop_column('games', 'ai_guesses')
    op.drop_column('games', 'player_secret')
