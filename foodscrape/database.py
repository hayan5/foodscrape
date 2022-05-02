from sqlalchemy.orm import Session, declarative_base

from .extensions import db

Model = db.Model
Base = declarative_base(metadata=db.metadata)
session: Session = db.session
