from foodscrape.database import Column, Model, db


class ScrapedIngredient(Model):
    __tablename__ = "scraped_ingredient"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, unique=True)
    times_seen = Column(db.Integer, default=1)

    db.UniqueConstraint(name)
