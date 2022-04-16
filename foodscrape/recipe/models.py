from foodscrape.database import Column, Model, db

recipe_keyword = db.Table(
    "recipe_keyword",
    db.Column("id", db.Integer, primary_key=True),
    db.Column(
        "keyword_id",
        db.Integer,
        db.ForeignKey("keyword.id", ondelete="CASCADE"),
        nullable=False,
    ),
    db.Column(
        "recipe_id",
        db.Integer,
        db.ForeignKey("recipe.id", ondelete="CASCADE"),
        nullable=False,
    ),
)


class Recipe(Model):  # type: ignore
    __tablename__ = "recipe"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String)
    date_published = Column(db.String)
    description = Column(db.String)
    image = Column(db.String)
    author = Column(db.String)
    recipe_category = Column(db.String)
    recipe_yield = Column(db.String)
    cook_time = Column(db.String)
    prep_time = Column(db.String)
    total_time = Column(db.String)
    rating = Column(db.String)

    keywords = db.relationship(
        "Keyword", secondary=recipe_keyword, back_populates="recipes"
    )

    instructions = db.relationship("Instruction", backref="recipe", lazy=True)
    # recipe_ingredients: List[Ingredient] = field(default_factory=list)


class Keyword(Model):
    __tablename__ = "recipe"

    id = Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    recipes = db.relationship(
        "Recipe", secondary=recipe_keyword, back_populates="keywords"
    )


class Instruction(db.Model):  # type: ignore
    __tablename__ = "instruction"

    id = db.Column(db.Integer, primary_key=True)
    seq_num = db.Column(db.Integer)
    text = db.Column(db.String)
    recipe_id = db.Column(
        db.Integer, db.ForeignKey("recipe.id"), nullable=False
    )
