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
    language = Language.query.get(language_id)
    return language_schema.dump(language)