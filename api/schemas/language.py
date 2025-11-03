from api.models.language import Language
from api.schemas import ma

class LanguageSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Language

language_schema = LanguageSchema()
languages_schema = LanguageSchema(many=True)