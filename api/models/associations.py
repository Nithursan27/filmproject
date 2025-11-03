from sqlalchemy import Column, Table, ForeignKey, Integer
from api.models import db
from sqlalchemy.orm import Mapped, relationship, mapped_column, DeclarativeBase

film_actor_table = db.Table(
    "film_actor",
    db.Column("actor_id", ForeignKey("actor.actor_id"), primary_key=True),
    db.Column("film_id", ForeignKey("film.film_id"), primary_key=True),
)