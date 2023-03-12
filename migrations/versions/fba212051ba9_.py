"""empty message

Revision ID: fba212051ba9
Revises: 5c3084c3c6d1
Create Date: 2023-03-11 21:04:25.018891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fba212051ba9'
down_revision = '5c3084c3c6d1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.drop_constraint('uq_students_student_no', type_='unique')

    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.drop_constraint('uq_teachers_teacher_no', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_teachers_teacher_no', ['teacher_no'])

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_students_student_no', ['student_no'])

    # ### end Alembic commands ###
