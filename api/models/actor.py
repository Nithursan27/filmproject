from api.models import db
from api.models.associations import film_actor_table
from api.models.film import Film

class Actor(db.Model):
    __tablename__ = "actor"
    
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    films = db.relationship("Film",
        secondary=film_actor_table, back_populates="actors"
    )
    
    