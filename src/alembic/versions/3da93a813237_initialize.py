"""initialize

Revision ID: 3da93a813237
Revises: 
Create Date: 2020-04-25 20:16:33.866466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3da93a813237'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('userextend',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('signature', sa.String(), nullable=True),
    sa.Column('self_introduction', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userextend_id'), 'userextend', ['id'], unique=False)
    op.create_table('userprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nick_name', sa.String(), nullable=True),
    sa.Column('telephone', sa.String(), nullable=True),
    sa.Column('avatar', sa.String(), nullable=True),
    sa.Column('age', sa.SMALLINT(), nullable=True),
    sa.Column('sex', sa.SMALLINT(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_userprofile_id'), 'userprofile', ['id'], unique=False)
    op.create_index(op.f('ix_userprofile_telephone'), 'userprofile', ['telephone'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_userprofile_telephone'), table_name='userprofile')
    op.drop_index(op.f('ix_userprofile_id'), table_name='userprofile')
    op.drop_table('userprofile')
    op.drop_index(op.f('ix_userextend_id'), table_name='userextend')
    op.drop_table('userextend')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
