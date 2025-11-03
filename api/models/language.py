from api.models import db
from sqlalchemy.orm import relationship, mapped_column, Mapped

class Language(db.Model):
    __tablename__ = "language"
    
    language_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)