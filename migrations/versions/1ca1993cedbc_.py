"""empty message

Revision ID: 1ca1993cedbc
Revises: 
Create Date: 2020-05-04 22:14:55.908734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ca1993cedbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('restaurantusers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('logo', sa.String(length=100), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('number_of_orders', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('order',
    sa.Column('id_order', sa.Integer(), nullable=False),
    sa.Column('order_number', sa.Integer(), nullable=True),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.Column('date_finalization', sa.DateTime(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('comment', sa.String(length=500), nullable=True),
    sa.Column('done', sa.String(length=100), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_restaurant', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_restaurant'], ['restaurantusers.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_order')
    )
    op.create_table('product',
    sa.Column('id_product', sa.Integer(), nullable=False),
    sa.Column('name_product', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('photo', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('id_restaurant', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_restaurant'], ['restaurantusers.id'], ),
    sa.PrimaryKeyConstraint('id_product')
    )
    op.create_table('ingredient',
    sa.Column('id_ingredinet', sa.Integer(), nullable=False),
    sa.Column('name_ingredinet', sa.String(length=100), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('id_product', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_product'], ['product.id_product'], ),
    sa.PrimaryKeyConstraint('id_ingredinet')
    )
    op.create_table('order_details',
    sa.Column('id_order_detail', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('product_name', sa.String(length=100), nullable=True),
    sa.Column('product_price', sa.String(length=100), nullable=True),
    sa.Column('id_product', sa.Integer(), nullable=True),
    sa.Column('id_order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_order'], ['order.id_order'], ),
    sa.ForeignKeyConstraint(['id_product'], ['product.id_product'], ),
    sa.PrimaryKeyConstraint('id_order_detail')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('ingredient')
    op.drop_table('product')
    op.drop_table('order')
    op.drop_table('users')
    op.drop_table('restaurantusers')
    op.drop_table('admins')
    # ### end Alembic commands ###
