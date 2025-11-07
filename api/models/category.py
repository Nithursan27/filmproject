from api.models import db
from sqlalchemy.orm import relationship, mapped_column, Mapped
from api.models.associations import film_category_table

class Category(db.Model):
    __tablename__ = "category"
    
    category_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    films = db.relationship("Film",
        secondary=film_category_table, back_populates="categories")