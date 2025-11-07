from api.models import db
from api.models.language import Language
from sqlalchemy import ForeignKey
from api.models.category import Category
from api.models.associations import film_actor_table, film_category_table
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Film(db.Model):
    __tablename__ = "film"
    
    film_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    release_year: Mapped[int] = mapped_column()
    language_id: Mapped[int] = mapped_column(ForeignKey("language.language_id"), nullable=False)
    language: Mapped["Language"] = relationship(foreign_keys=[language_id])
    original_language_id: Mapped["Language"] = mapped_column(ForeignKey("language.language_id"), nullable=True)
    rental_duration: Mapped[int] = mapped_column(nullable=False, default=3)
    rental_rate: Mapped[float] = mapped_column(nullable=False, default=4.99)
    length: Mapped[int] = mapped_column(nullable=True)
    replacement_cost: Mapped[float] = mapped_column(nullable=False, default=19.99)
    rating: Mapped[str] = mapped_column(default="G")
    special_features: Mapped[str] = mapped_column(nullable=True)
    actors = db.relationship("Actor",
        secondary=film_actor_table, back_populates="films"
    )
    categories = db.relationship("Category",
        secondary=film_category_table, back_populates="films")