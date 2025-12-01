"""seed default models

Revision ID: cae28a432591
Revises: 4f9973f7f7f0
Create Date: 2025-12-01 10:32:54.243110

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from models.chat.model import Model
import os


# revision identifiers, used by Alembic.
revision = 'cae28a432591'
down_revision = '4f9973f7f7f0'
branch_labels = None
depends_on = None


Base = declarative_base()
default_models_str = os.environ.get('DEFAULT_MODELS') or ["qwen3-embedding:0.6b", "qwen/qwen3-coder"]


def upgrade() -> None:
    bind = op.get_bind()
    Session = sessionmaker(bind=bind)
    session = Session()

    if default_models_str:
        model_names = [name.strip() for name in default_models_str if name.strip()]
        for model_name in model_names:
            existing_model = session.query(Model).filter_by(model_name=model_name).first()
            if not existing_model:
                new_model = Model(model_name=model_name)
                session.add(new_model)
    session.commit()
    session.close()


def downgrade() -> None:
    bind = op.get_bind()
    Session = sessionmaker(bind=bind)
    session = Session()

    default_models_str = os.environ.get('DEFAULT_MODELS')
    if default_models_str:
        model_names = [name.strip() for name in default_models_str.split(',') if name.strip()]
        for model_name in model_names:
            session.query(Model).filter_by(model_name=model_name).delete()
    session.commit()
    session.close()