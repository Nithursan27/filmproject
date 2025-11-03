from api.models.actor import Actor
from api.schemas.film import films_schema
from api.schemas import ma
from marshmallow_sqlalchemy import fields
from flask import url_for

class ActorSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Actor
        include_relationships=True
        
    films = fields.Nested(films_schema, only=("film_id", "title"))

actor_schema = ActorSchema()
actors_schema = ActorSchema(many=True)