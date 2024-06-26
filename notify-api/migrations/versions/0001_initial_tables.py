"""Initial tables

Revision ID: 4273ebef85cc
Revises:
Create Date: 2019-11-08 16:11:30.331270

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Boolean, String
from sqlalchemy.sql import column, table


# revision identifiers, used by Alembic.
revision = "4273ebef85cc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "notification_status",
        sa.Column("code", sa.String(length=15), nullable=False),
        sa.Column("desc", sa.String(length=100), nullable=True),
        sa.Column("default", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_table(
        "notification_type",
        sa.Column("code", sa.String(length=15), nullable=False),
        sa.Column("desc", sa.String(length=100), nullable=True),
        sa.Column("default", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("code"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "notification",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipients", sa.String(length=2000), nullable=False),
        sa.Column("request_date", sa.DateTime(), nullable=False),
        sa.Column("sent_date", sa.DateTime(), nullable=True),
        sa.Column("type_code", sa.String(length=15), nullable=False),
        sa.Column("status_code", sa.String(length=15), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_code"],
            ["notification_status.code"],
        ),
        sa.ForeignKeyConstraint(
            ["type_code"],
            ["notification_type.code"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "notification_contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("subject", sa.String(length=2000), nullable=False),
        sa.Column("body", sa.String(length=2000), nullable=False),
        sa.Column("attachment_name", sa.String(length=200), nullable=True),
        sa.Column("attachment", sa.LargeBinary(), nullable=True),
        sa.Column("notification_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["notification_id"],
            ["notification.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    notification_type_table = table(
        "notification_type", column("code", String), column("desc", String), column("default", Boolean)
    )

    op.bulk_insert(
        notification_type_table,
        [
            {"code": "EMAIL", "desc": "The Email type of notification", "default": True},
            {"code": "TEXT", "desc": "The Text message type of notification", "default": False},
        ],
    )

    # Insert codes and descriptions for organization status
    notification_status_table = table(
        "notification_status", column("code", String), column("desc", String), column("default", Boolean)
    )
    op.bulk_insert(
        notification_status_table,
        [
            {"code": "PENDING", "desc": "Initial state of the notification", "default": True},
            {"code": "DELIVERED", "desc": "Status for the notification delivered successful", "default": False},
            {"code": "FAILURE", "desc": "Status for the notification sent failure", "default": False},
            {"code": "SENT", "desc": "Status for the notification sent successful", "default": False},
            {"code": "QUEUED", "desc": "Status for the notification get queued", "default": False},
        ],
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("notification_contents")
    op.drop_table("notification")
    op.drop_table("notification_type")
    op.drop_table("notification_status")
    # ### end Alembic commands ###
