from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from api.models import db
from api.models.language import Language
from api.schemas.language import language_schema, languages_schema

languages_router = Blueprint('languages', __name__, url_prefix='/languages')

@languages_router.get('/')
def read_all_languages():
    languages = Language.query.all()
    return languages_schema.dump(languages)

@languages_router.get('/<language_id>')
def read_language(language_id):
    language = Language.query.get_or_404(language_id)
    return language_schema.dump(language)

@languages_router.post('/')
def create_language():
    language_data = request.json
    
    try:
        language_schema.load(language_data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    language = Language(**language_data)
    db.session.add(language)
    db.session.commit()

    return language_schema.dump(language)

@languages_router.delete('/<language_id>')
def delete_language(language_id):
    language = Language.query.get_or_404(language_id)
    db.session.delete(language)
    db.session.commit()

    return ("", 204)