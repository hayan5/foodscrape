from foodscrape.database import Column, Model, db


class RawIngredient(Model):
    __tablename__ = "raw_ingredient"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, unique=True)

    db.UniqueConstraint(name)
