"""empty message

Revision ID: ef9c569eabb8
Revises: 
Create Date: 2024-09-16 17:22:29.363385

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9c569eabb8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('boulder')
    op.drop_table('user')
    op.drop_table('attempt')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attempt',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('number_of_attempts', sa.INTEGER(), nullable=False),
    sa.Column('status', sa.TEXT(), nullable=False),
    sa.Column('attempt_date', sa.DATE(), server_default=sa.text("(DATE('now'))"), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('boulder_id', sa.INTEGER(), nullable=False),
    sa.Column('moves_completed', sa.INTEGER(), nullable=True),
    sa.Column('difficulty', sa.INTEGER(), nullable=False),
    sa.CheckConstraint("status IN ('incomplete', 'completed', 'flashed')) NOT NULL,\r\n    attempt_date DATE DEFAULT (DATE('now')),\r\n    user_id INTEGER NOT NULL,\r\n    boulder_id INTEGER NOT NULL,\r\n    moves_completed INTEGER,\r\n    difficulty INTEGER NOT NULL,  -- Store the difficulty of the boulder when this attempt was made\r\n    FOREIGN KEY (user_id) REFERENCES user(id"),
    sa.ForeignKeyConstraint(['boulder_id'], ['boulder.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('username', sa.TEXT(), nullable=False),
    sa.Column('firstname', sa.TEXT(), nullable=False),
    sa.Column('lastname', sa.TEXT(), nullable=False),
    sa.Column('email', sa.TEXT(), nullable=False),
    sa.Column('password', sa.TEXT(), nullable=False),
    sa.Column('gender', sa.TEXT(), nullable=False),
    sa.Column('age', sa.TEXT(), nullable=False),
    sa.Column('profile_picture', sa.TEXT(), nullable=True),
    sa.Column('highest_grade_climbed', sa.INTEGER(), server_default=sa.text('0'), nullable=True),
    sa.Column('highest_grade_flashed', sa.INTEGER(), server_default=sa.text('0'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('boulder',
    sa.Column('id', sa.INTEGER(), nullable=True),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('color', sa.TEXT(), nullable=False),
    sa.Column('difficulty', sa.INTEGER(), nullable=False),
    sa.Column('numberofmoves', sa.INTEGER(), nullable=False),
    sa.Column('set_date', sa.DATE(), nullable=True),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('image', sa.TEXT(), nullable=True),
    sa.Column('created_by', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
