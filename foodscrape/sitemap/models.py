import datetime as dt

from foodscrape.database import Column, Model, db


class Sitemap(Model):
    __tablename__ = "sitemap"

    id = Column(db.Integer, primary_key=True)
    url = Column(db.String, unique=True, nullable=False)
    is_scraped = Column(db.Boolean, default=False)
    scraped_date = Column(db.DateTime)
    created_at = Column(db.DateTime, default=dt.datetime.utcnow())
    updated_at = Column(db.DateTime, default=dt.datetime.utcnow())

    db.UniqueConstraint(url)
