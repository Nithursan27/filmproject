from api.models.film import Film
from api.models.language import Language
from api.schemas.language import LanguageSchema
from api.schemas.category import categorys_schema
from api.schemas import ma
from marshmallow import ValidationError, fields, validate, validates
from marshmallow_sqlalchemy import auto_field

RATINGS = ["G", "PG", "PG-13", "R", "NC-17"]
SPECIAL_FEATURES = set(["Trailers", "Commentaries", "Deleted Scenes", "Behind the Scenes"])
    
class FilmSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Film
        include_relationships=True
        load_instance = True
        
    description = fields.String(allow_none=True)
    release_year= fields.Integer(allow_none=True)
    language_id = fields.Integer(validate=validate.Range(min=1, max=255), load_only=True, required=True)
    original_language_id = fields.Integer(validate=validate.Range(min=1, max=255), allow_none=True)
    rental_duration = fields.Integer(validate=validate.Range(min=1, max=255))
    rental_rate = fields.Decimal(places=2, validate=validate.Range(min=0.0, max=99.99, max_inclusive=True))
    length = fields.Integer(validate=validate.Range(min=1, max=65535), allow_none=True)
    replacement_cost= fields.Decimal(places=2, validate=validate.Range(min=0.0, max=999.99, max_inclusive=True))
    rating = fields.String(validate=validate.OneOf(RATINGS))
    
    language = fields.Nested(LanguageSchema)
    actors = fields.Nested("ActorSchema", many=True, only=("actor_id", "first_name", "last_name"), dump_only=True)
    categories = fields.Nested(categorys_schema, dump_only=True)
    
    @validates('special_features')
    def validate_special_features(self, value, **kwargs):
        if value:
            for feature in value.split(","):
                if feature not in SPECIAL_FEATURES:
                    raise ValidationError("Invalid special feature in list. Please ensure there are no spaces between commas separating values")
    
film_schema = FilmSchema()
films_schema = FilmSchema(many=True)