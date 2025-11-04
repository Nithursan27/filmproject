from api.models.film import Film
from api.models.language import Language
from api.schemas.language import LanguageSchema
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
    language_id = fields.Integer(validate=validate.Range(min=1, max=255), load_only=True)
    original_language_id = fields.Integer(validate=validate.Range(min=1, max=255), allow_none=True)
    rental_duration = fields.Integer(validate=validate.Range(min=1, max=255))
    rental_rate = fields.Float(validate=validate.Range(min=0.0, max=10000.0, max_inclusive=False))
    length = fields.Integer(validate=validate.Range(min=1, max=65535), allow_none=True)
    replacement_cost= fields.Float(validate=validate.Range(min=0.0, max=100000.0, max_inclusive=False))
    rating= fields.String(validate=validate.OneOf(RATINGS), required=True)
    language = fields.Nested(LanguageSchema)
    
    @validates('special_features')
    def validate_special_features(self, value, **kwargs):
        if value:
            for feature in value.split(","):
                if feature not in SPECIAL_FEATURES:
                    raise ValidationError("Invalid special feature in list. Please ensure there are no spaces between commas separating values")
    
film_schema = FilmSchema()
films_schema = FilmSchema(many=True)