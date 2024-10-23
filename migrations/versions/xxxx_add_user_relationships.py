from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create users table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(120), nullable=False),
        sa.Column('password_hash', sa.String(200)),
        sa.Column('name', sa.String(100)),
        sa.Column('role', sa.String(50)),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Add user_id to projects
    op.add_column('project',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id'))
    )

def downgrade():
    op.drop_column('project', 'user_id')
    op.drop_table('user')
