import json

from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:password@127.0.0.1:5433/foodscrape"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secret string"

db: SQLAlchemy = SQLAlchemy(app)

migrate = Migrate(app, db)


class Ingredient(db.Model):  # type: ignore
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    name = Column(String)


@app.route("/", methods=["POST"])
def index():
    data = json.loads(request.data.decode())
    name = data["name"]
    from app import db

    # save the results
    errors = []
    try:
        result = Ingredient(
            name=name,
        )
        db.session.add(result)
        db.session.commit()
        return str(result.id)
    except:
        errors.append("Unable to add item to database.")
        return {"error": errors}


if __name__ == "__main__":
    app.run()
